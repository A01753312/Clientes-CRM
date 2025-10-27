"""Funciones auxiliares generales"""
import re
import unicodedata
from pathlib import Path

SAFE_NAME_RE = re.compile(r"[^A-Za-z0-9._\-áéíóúÁÉÍÓÚñÑ ]+")

def safe_name(s: str) -> str:
    if s is None:
        return ""
    s = str(s).strip()
    s = SAFE_NAME_RE.sub("_", s)
    s = re.sub(r"\s+", " ", s)
    return s[:150]


def normalize_key(s: str) -> str:
    s = str(s or "").strip()
    s = re.sub(r"\s+", " ", s)
    s = unicodedata.normalize("NFKD", s)
    s = "".join(ch for ch in s if not unicodedata.combining(ch))
    return s.casefold()


def canonicalize_from_catalog(value: str, catalog: list, extra_synonyms: dict | None = None, min_ratio: float = 0.85) -> str:
    """Match a free-text `value` to the closest entry in `catalog` using fuzzy matching.

    Returns the best match from catalog or the original value if no good match is found.
    """
    try:
        import difflib
        v = (value or "").strip()
        if not v:
            return ""
        # Check exact
        for c in catalog:
            if str(c).strip() == v:
                return c
        # check synonyms
        if extra_synonyms:
            for k, syns in (extra_synonyms or {}).items():
                if v in syns:
                    return k
        # fuzzy
        matches = difflib.get_close_matches(v, [str(c) for c in catalog], n=1, cutoff=min_ratio)
        if matches:
            return matches[0]
    except Exception:
        pass
    return value


def optimize_dataframe_memory(df):
    """Lightweight memory optimizer: downcast numeric types and convert object columns with few uniques to category."""
    try:
        import numpy as np
        df = df.copy()
        for col in df.select_dtypes(include=['int64', 'float64']).columns:
            try:
                df[col] = pd.to_numeric(df[col], downcast='unsigned')
            except Exception:
                try:
                    df[col] = pd.to_numeric(df[col], downcast='float')
                except Exception:
                    pass
        for col in df.select_dtypes(include=['object']).columns:
            try:
                nunique = df[col].nunique(dropna=True)
                if nunique > 0 and (nunique / max(1, len(df)) ) < 0.5:
                    df[col] = df[col].astype('category')
            except Exception:
                pass
        return df
    except Exception:
        return df


def find_logo() -> Path | None:
    from crm_project.config.settings import DATA_DIR
    for ext in ["png", "jpg", "jpeg"]:
        logo = DATA_DIR / f"logo.{ext}"
        if logo.exists():
            return logo
    return None


def do_rerun():
    try:
        import streamlit as st
        if hasattr(st, "rerun"):
            st.rerun()
            return
        if hasattr(st, "experimental_rerun"):
            st.experimental_rerun()
            return
    except Exception:
        try:
            import streamlit as st
            st.session_state["_need_rerun"] = True
        except Exception:
            pass
