"""Operaciones CRUD para clientes"""
import pandas as pd
import streamlit as st
from pathlib import Path
from typing import Optional
from crm_project.config.settings import (
    CLIENTES_CSV, CLIENTES_XLSX, COLUMNS, HISTORIAL_CSV, DOCS_DIR
)
from crm_project.utils.helpers import safe_name
import shutil

class ClienteDB:
    @staticmethod
    @st.cache_data(ttl=60, show_spinner=False)
    def cargar_clientes() -> pd.DataFrame:
        def _ensure_cols(df: pd.DataFrame) -> pd.DataFrame:
            df = df.copy().fillna("")
            for c in COLUMNS:
                if c not in df.columns:
                    df[c] = ""
            return df[[c for c in COLUMNS if c in df.columns]]
        try:
            if CLIENTES_XLSX.exists():
                df = pd.read_excel(CLIENTES_XLSX, dtype=str).fillna("")
                return _ensure_cols(df)
        except Exception:
            pass
        try:
            if CLIENTES_CSV.exists():
                df = pd.read_csv(CLIENTES_CSV, dtype=str).fillna("")
                return _ensure_cols(df)
        except Exception:
            pass
        return pd.DataFrame(columns=COLUMNS)

    @staticmethod
    def guardar_clientes(df: pd.DataFrame):
        if df is None:
            return
        for c in COLUMNS:
            if c not in df.columns:
                df[c] = ""
        df_to_save = df[[c for c in COLUMNS if c in df.columns]].copy().fillna("").astype(str)
        try:
            df_to_save.to_csv(CLIENTES_CSV, index=False, encoding="utf-8")
        except Exception as e:
            try:
                st.error(f"Error guardando CSV: {e}")
            except Exception:
                pass
        try:
            engine = "openpyxl"
            with pd.ExcelWriter(CLIENTES_XLSX, engine=engine) as writer:
                df_to_save.to_excel(writer, index=False, sheet_name="Clientes")
        except Exception:
            pass
        ClienteDB.cargar_clientes.clear()

    @staticmethod
    def nuevo_id(df: pd.DataFrame) -> str:
        base_id = 1000
        try:
            if not df.empty and "id" in df.columns:
                nums = []
                for x in df["id"].astype(str):
                    if x.startswith("C"):
                        try:
                            nums.append(int(x[1:]))
                        except Exception:
                            continue
                if nums:
                    base_id = max(nums) + 1
        except Exception:
            pass
        return f"C{base_id}"

    @staticmethod
    def eliminar_cliente(cid: str, df: pd.DataFrame) -> pd.DataFrame:
        if not cid or df.empty:
            return df
        try:
            folder = DOCS_DIR / safe_name(cid)
            if folder.exists():
                shutil.rmtree(folder)
        except Exception:
            pass
        df_new = df[df["id"] != cid].reset_index(drop=True)
        ClienteDB.guardar_clientes(df_new)
        return df_new

class HistorialDB:
    @staticmethod
    def cargar_historial() -> pd.DataFrame:
        cols = [
            "id", "nombre", "estatus_old", "estatus_new",
            "segundo_old", "segundo_new", "observaciones",
            "action", "actor", "ts"
        ]
        try:
            if HISTORIAL_CSV.exists():
                dfh = pd.read_csv(HISTORIAL_CSV, dtype=str).fillna("")
                for c in cols:
                    if c not in dfh.columns:
                        dfh[c] = ""
                return dfh[cols]
        except Exception:
            pass
        return pd.DataFrame(columns=cols)

    @staticmethod
    def append_historial(
        cid: str, nombre: str, estatus_old: str, estatus_new: str,
        seg_old: str, seg_new: str, observaciones: str = "",
        action: str = "ESTATUS MODIFICADO", actor: Optional[str] = None
    ):
        if actor is None:
            actor = "(sistema)"
        registro = {
            "id": cid,
            "nombre": nombre or "",
            "estatus_old": estatus_old or "",
            "estatus_new": estatus_new or "",
            "segundo_old": seg_old or "",
            "segundo_new": seg_new or "",
            "observaciones": observaciones or "",
            "action": action or "",
            "actor": actor or "",
            "ts": pd.Timestamp.now().isoformat()
        }
        try:
            if HISTORIAL_CSV.exists():
                dfh = HistorialDB.cargar_historial()
                dfh = pd.concat([dfh, pd.DataFrame([registro])], ignore_index=True)
            else:
                dfh = pd.DataFrame([registro])
            dfh.to_csv(HISTORIAL_CSV, index=False, encoding="utf-8")
        except Exception:
            pass
