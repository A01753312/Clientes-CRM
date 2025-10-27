"""Componente de sidebar con filtros"""
import streamlit as st
import pandas as pd
from crm_project.core.auth import AuthSession
from crm_project.core.database import ClienteDB
from crm_project.config.settings import SUCURSALES, ESTATUS_OPCIONES
from crm_project.utils.helpers import do_rerun


def render_sidebar() -> pd.DataFrame:
    user = AuthSession.current_user()
    st.sidebar.markdown(f"**Usuario:** {(user or {}).get('user','(anónimo)')} — _{(user or {}).get('role','member')}_")
    if st.sidebar.button("Cerrar sesión"):
        AuthSession.logout()
        do_rerun()
    df = ClienteDB.cargar_clientes()
    st.sidebar.title("🔍 Filtros")
    sucursales = st.sidebar.multiselect(
        "Sucursales",
        options=SUCURSALES,
        default=SUCURSALES,
        key="f_sucursales"
    )
    estatus = st.sidebar.multiselect(
        "Estatus",
        options=ESTATUS_OPCIONES,
        default=ESTATUS_OPCIONES,
        key="f_estatus"
    )
    try:
        df_filtrado = df[
            df["sucursal"].isin(sucursales) & df["estatus"].isin(estatus)
        ]
    except Exception:
        df_filtrado = df.copy()
    st.sidebar.markdown("---")
    st.sidebar.metric("Clientes visibles", len(df_filtrado))
    st.sidebar.metric("Total en base", len(df))
    return df_filtrado
