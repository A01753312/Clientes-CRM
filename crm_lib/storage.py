import json
from pathlib import Path
import pandas as pd
from .config import CLIENTES_CSV, CLIENTES_XLSX, HISTORIAL_CSV

COLUMNS = [
    "id","nombre","sucursal","asesor","fecha_ingreso","fecha_dispersion",
    "estatus","monto_propuesta","monto_final","segundo_estatus","observaciones",
    "score","telefono","correo","analista","fuente"
]

def cargar_clientes_local() -> pd.DataFrame:
    try:
        if CLIENTES_XLSX.exists():
            df = pd.read_excel(CLIENTES_XLSX, dtype=str).fillna("")
            for c in COLUMNS:
                if c not in df.columns:
                    df[c] = ""
            return df[[c for c in COLUMNS if c in df.columns]]
    except Exception:
        pass
    try:
        if CLIENTES_CSV.exists():
            df = pd.read_csv(CLIENTES_CSV, dtype=str).fillna("")
            for c in COLUMNS:
                if c not in df.columns:
                    df[c] = ""
            return df[[c for c in COLUMNS if c in df.columns]]
    except Exception:
        pass
    return pd.DataFrame(columns=COLUMNS)

def guardar_clientes_local(df: pd.DataFrame):
    if df is None:
        return
    for c in COLUMNS:
        if c not in df.columns:
            df[c] = ""
    df_to_save = df[[c for c in COLUMNS if c in df.columns]].copy().fillna("").astype(str)
    try:
        df_to_save.to_csv(CLIENTES_CSV, index=False, encoding="utf-8")
    except Exception:
        pass
    try:
        with pd.ExcelWriter(CLIENTES_XLSX, engine="openpyxl") as writer:
            df_to_save.to_excel(writer, index=False, sheet_name="Clientes")
    except Exception:
        pass

def cargar_historial_local() -> pd.DataFrame:
    cols = ["id","nombre","estatus_old","estatus_new","segundo_old","segundo_new","observaciones","action","actor","ts"]
    try:
        if HISTORIAL_CSV.exists():
            df = pd.read_csv(HISTORIAL_CSV, dtype=str).fillna("")
            for c in cols:
                if c not in df.columns:
                    df[c] = ""
            return df[cols].copy()
    except Exception:
        pass
    return pd.DataFrame(columns=cols)

def guardar_historial_local(dfh: pd.DataFrame):
    try:
        dfh.to_csv(HISTORIAL_CSV, index=False, encoding="utf-8")
    except Exception:
        pass
