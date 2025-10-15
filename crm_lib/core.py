import re
import unicodedata
from typing import Optional
import pandas as pd

def _norm_key(s: str) -> str:
    s = (s or "").strip()
    s = re.sub(r"\s+", " ", s)
    s = unicodedata.normalize("NFKD", s)
    s = "".join(ch for ch in s if not unicodedata.combining(ch))
    return s.casefold()


def find_matching_asesor(name: str, df: pd.DataFrame) -> str:
    name = (name or "").strip()
    if not name:
        return ""
    name_key = _norm_key(name)
    for a in df["asesor"].fillna("").unique():
        if not str(a).strip():
            continue
        if _norm_key(a) == name_key:
            return a
    return " ".join(w.capitalize() for w in name.split())


def nuevo_id_cliente(df: Optional[pd.DataFrame]) -> str:
    base_id = 1000
    try:
        if df is not None and not getattr(df, 'empty', True) and "id" in df.columns:
            nums = []
            for x in df["id"].astype(str):
                if not x:
                    continue
                m = None
                try:
                    import re as _re
                    m = _re.match(r"^C(\d+)$", str(x).strip())
                except Exception:
                    m = None
                if m:
                    try:
                        nums.append(int(m.group(1)))
                    except Exception:
                        continue
            if nums:
                base_id = max(nums) + 1
            else:
                base_id = base_id + len(df)
    except Exception:
        pass
    return f"C{base_id}"
