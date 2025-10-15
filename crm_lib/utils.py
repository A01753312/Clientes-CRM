import re
import difflib
import unicodedata
from pathlib import Path
from typing import List
import pandas as pd

SAFE_NAME_RE = re.compile(r"[^A-Za-z0-9._\\\-áéíóúÁÉÍÓÚñÑ ]+")

def safe_name(s: str) -> str:
    if s is None:
        return ""
    s = str(s).strip()
    s = SAFE_NAME_RE.sub("_", s)
    s = re.sub(r"\s+", " ", s)
    return s[:150]


def sort_df_by_dates(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    date_cols = [col for col in ["fecha_ingreso", "fecha_dispersion", "ts"] if col in df.columns]
    for col in date_cols:
        try:
            df[col] = pd.to_datetime(df[col], errors="coerce")
        except Exception:
            pass
    if date_cols:
        return df.sort_values(date_cols, ascending=True, na_position="last").reset_index(drop=True)
    return df


def canonicalize_from_catalog(raw: str, catalog: List[str], extra_synonyms: dict | None = None, min_ratio: float = 0.90) -> str:
    s = (raw or "").strip()
    if not s:
        return s
    def _norm_key(sv: str) -> str:
        sv = (sv or "").strip()
        sv = re.sub(r"\s+", " ", sv)
        sv = unicodedata.normalize("NFKD", sv)
        sv = "".join(ch for ch in sv if not unicodedata.combining(ch))
        return sv.casefold()

    key = _norm_key(s)
    # exact match
    for opt in catalog:
        if _norm_key(opt) == key:
            return opt
    # synonyms
    if extra_synonyms:
        for k, v in extra_synonyms.items():
            if _norm_key(k) == key:
                for opt in catalog:
                    if _norm_key(opt) == _norm_key(v):
                        return opt
                return v
    # fuzzy
    best, best_r = None, 0.0
    for opt in catalog:
        r = difflib.SequenceMatcher(None, key, _norm_key(opt)).ratio()
        if r > best_r:
            best_r, best = r, opt
    if best and best_r >= min_ratio:
        return best
    return s


def optimize_dataframe_memory(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    for col in ["estatus","segundo_estatus","sucursal","asesor","analista","fuente"]:
        if col in df.columns:
            try:
                df[col] = df[col].astype("category")
            except Exception:
                pass
    for col in ["monto_propuesta","monto_final","score"]:
        if col in df.columns:
            try:
                df[col] = pd.to_numeric(df[col], errors="coerce").astype("float32")
            except Exception:
                pass
    return df
