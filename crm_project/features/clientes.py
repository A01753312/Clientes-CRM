"""Tab de Clientes: alta, edición y lista (migración desde crm.py)

Este módulo expone `render(...)` que es invocado desde `crm.py`.
Se espera recibir las dependencias (funciones y constantes) como parámetros
para evitar import cycles durante la migración incremental.
"""
from typing import Callable
import streamlit as st
import pandas as pd
from crm_project.utils.helpers import safe_name


def render(
    df_cli: pd.DataFrame,
    df_ver: pd.DataFrame,
    guardar_clientes: Callable[[pd.DataFrame], None],
    subir_docs: Callable,
    append_historial: Callable,
    create_backup_zip: Callable,
    git_auto_commit: Callable,
    do_rerun: Callable,
    find_matching_asesor: Callable,
    nuevo_id_cliente: Callable,
    get_nombre_by_id: Callable,
    get_field_by_id: Callable,
    SUCURSALES,
    ESTATUS_OPCIONES,
    SEGUNDO_ESTATUS_OPCIONES,
    DOC_CATEGORIAS,
    COLUMNS,
    can: Callable,
):
    """Renderiza la pestaña Clientes (alta y lista básica).

    Notas:
    - Intenta conservar la lógica original pero con una implementación más
      compacta y clara para facilitar tests y migración.
    - `df_cli` es la base completa; `df_ver` es la vista filtrada que se muestra.
    """

    st.subheader("➕ Agregar cliente")
    with st.expander("Formulario de alta", expanded=False):
        st.checkbox("Nuevo asesor (marca para escribir nombre y apellido)", key="form_new_asesor_toggle")
        if st.session_state.get("form_new_asesor_toggle", False):
            st.text_input("Nombre y apellido del nuevo asesor", placeholder="Ej. Juan Pérez", key="form_nuevo_asesor")

        with st.form("form_alta_cliente", clear_on_submit=True):
            c1, c2, c3 = st.columns(3)
            with c1:
                id_n = st.text_input("ID (opcional)", key="form_id")
                nombre_n = st.text_input("Nombre *")
                sucursal_n = st.selectbox("Sucursal *", SUCURSALES)
                raw_ases = [a for a in df_cli.get("asesor", pd.Series()).fillna("").unique() if str(a).strip()]
                asesores_exist = sorted(list(dict.fromkeys([str(a).strip() or "(Sin asesor)" for a in raw_ases])))
                asesor_select = st.selectbox("Asesor", ["(Sin asesor)"] + asesores_exist, key="form_ases_select")
                if st.session_state.get("form_new_asesor_toggle", False):
                    asesor_n = st.session_state.get("form_nuevo_asesor", "").strip()
                else:
                    asesor_n = "" if asesor_select == "(Sin asesor)" else asesor_select
                analista_n = st.text_input("Analista")
            with c2:
                fecha_ingreso_n = st.date_input("Fecha ingreso")
                fecha_dispersion_n = st.date_input("Fecha dispersión")
                estatus_n = st.selectbox("Estatus", ESTATUS_OPCIONES, index=0)
                segundo_estatus_n = st.selectbox("Segundo estatus", SEGUNDO_ESTATUS_OPCIONES, index=0)
            with c3:
                monto_prop_n = st.text_input("Monto propuesta", value="")
                monto_final_n = st.text_input("Monto final", value="")
                score_n = st.text_input("Score", value="")
                telefono_n = st.text_input("Teléfono")
                correo_n = st.text_input("Correo")
                fuente_n = st.text_input("Fuente", value="")
            obs_n = st.text_area("Observaciones")

            up_estado = st.file_uploader("Estado de cuenta", type=DOC_CATEGORIAS.get("estado_cuenta"), accept_multiple_files=True, key="doc_estado")
            up_buro   = st.file_uploader("Buró de crédito", type=DOC_CATEGORIAS.get("buro_credito"), accept_multiple_files=True, key="doc_buro")
            up_solic  = st.file_uploader("Solicitud", type=DOC_CATEGORIAS.get("solicitud"), accept_multiple_files=True, key="doc_solic")
            up_otros = st.file_uploader("Otros", type=None, accept_multiple_files=True, key="doc_otros")

            if st.form_submit_button("Guardar cliente"):
                if not nombre_n.strip():
                    st.warning("El nombre es obligatorio.")
                else:
                    # Generar o validar ID
                    provided = (id_n or "").strip()
                    if provided:
                        cid_candidate = safe_name(provided)
                        if cid_candidate in df_cli.get("id", pd.Series()).astype(str).tolist():
                            st.warning(f"El ID '{cid_candidate}' ya existe. Elige otro o deja vacío para generar uno.")
                            st.stop()
                        cid = cid_candidate
                    else:
                        cid = nuevo_id_cliente(df_cli)

                    asesor_final = find_matching_asesor(asesor_n.strip(), df_cli)
                    nuevo = {
                        "id": cid,
                        "nombre": nombre_n.strip(),
                        "sucursal": sucursal_n,
                        "asesor": asesor_final,
                        "fecha_ingreso": str(fecha_ingreso_n),
                        "fecha_dispersion": str(fecha_dispersion_n),
                        "estatus": estatus_n,
                        "monto_propuesta": str(monto_prop_n).strip(),
                        "monto_final": str(monto_final_n).strip(),
                        "segundo_estatus": segundo_estatus_n,
                        "observaciones": obs_n.strip(),
                        "score": str(score_n).strip(),
                        "telefono": telefono_n.strip(),
                        "correo": correo_n.strip(),
                        "analista": analista_n.strip(),
                        "fuente": fuente_n.strip(),
                    }
                    base = pd.concat([df_cli, pd.DataFrame([nuevo])], ignore_index=True)
                    try:
                        guardar_clientes(base)
                        st.session_state["cli_cache_ver"] = st.session_state.get("cli_cache_ver", 0) + 1
                    except Exception as e:
                        st.error(f"Error guardando cliente: {e}")

                    # Subir docs y registrar historial
                    subidos_lote = []
                    if up_estado:   subidos_lote += subir_docs(cid, up_estado,   prefijo="estado_")
                    if up_buro:     subidos_lote += subir_docs(cid, up_buro,     prefijo="buro_")
                    if up_solic:    subidos_lote += subir_docs(cid, up_solic,    prefijo="solic_")
                    if up_otros:    subidos_lote += subir_docs(cid, up_otros,    prefijo="otros_")

                    if subidos_lote:
                        actor = (st.session_state.get("auth_user") or {}).get("user")
                        try:
                            append_historial(cid, nuevo.get("nombre",""), "", nuevo.get("estatus",""), "", nuevo.get("segundo_estatus",""), f"Subidos: {', '.join(subidos_lote)}", action="DOCUMENTOS", actor=actor)
                        except Exception:
                            pass

                        # backup automático
                        try:
                            zip_path = create_backup_zip()
                            msg = git_auto_commit(zip_path)
                            st.success(f"Backup realizado: {msg}")
                        except Exception:
                            pass

                    st.success(f"Cliente {cid} creado ✅")
                    do_rerun()

    st.subheader("📋 Lista de clientes")
    if df_ver is None or df_ver.empty:
        st.info("No hay clientes con los filtros seleccionados.")
        return

    colcfg = {
        "id": st.column_config.TextColumn("ID", disabled=True),
        "nombre": st.column_config.TextColumn("Nombre"),
        "sucursal": st.column_config.SelectboxColumn("Sucursal", options=[""]+list(SUCURSALES), required=False),
        "asesor": st.column_config.TextColumn("Asesor"),
        "fecha_ingreso": st.column_config.TextColumn("Fecha ingreso (YYYY-MM-DD)"),
        "fecha_dispersion": st.column_config.TextColumn("Fecha dispersión (YYYY-MM-DD)"),
        "estatus": st.column_config.SelectboxColumn("Estatus", options=ESTATUS_OPCIONES, required=True),
        "monto_propuesta": st.column_config.TextColumn("Monto propuesta"),
        "monto_final": st.column_config.TextColumn("Monto final"),
        "segundo_estatus": st.column_config.SelectboxColumn("Segundo estatus", options=SEGUNDO_ESTATUS_OPCIONES),
        "observaciones": st.column_config.TextColumn("Observaciones"),
        "score": st.column_config.TextColumn("Score"),
        "telefono": st.column_config.TextColumn("Teléfono"),
        "correo": st.column_config.TextColumn("Correo"),
        "analista": st.column_config.TextColumn("Analista"),
        "fuente": st.column_config.TextColumn("Fuente"),
    }

    # Normalizar y ordenar
    try:
        df_show = df_ver.copy()
        for _dcol in ("fecha_ingreso", "fecha_dispersion"):
            if _dcol in df_show.columns:
                try:
                    df_show[_dcol] = pd.to_datetime(df_show[_dcol], errors="coerce").dt.date.astype(str).replace("NaT", "")
                except Exception:
                    df_show[_dcol] = df_show[_dcol].astype(str).fillna("")
    except Exception:
        df_show = df_ver.copy()

    ed = st.data_editor(df_show, use_container_width=True, hide_index=True, column_config=colcfg, key="editor_clientes")

    # Guardar cambios desde el editor
    if st.button("💾 Guardar cambios"):
        try:
            base = df_cli.set_index("id")
            for _, row in ed.iterrows():
                cid = row["id"]
                for k in COLUMNS:
                    if k == "id":
                        continue
                    base.at[cid, k] = str(row.get(k, ""))
            # Normalizar asesores
            for idx in base.index:
                base.at[idx, "asesor"] = find_matching_asesor(base.at[idx, "asesor"], base.reset_index())
            df_new = base.reset_index()
            guardar_clientes(df_new)
            st.session_state["cli_cache_ver"] = st.session_state.get("cli_cache_ver", 0) + 1
            st.success("Cambios guardados ✅")
            do_rerun()
        except Exception as e:
            st.error(f"Error guardando cambios: {e}")
