"""Core helpers exported for compatibility with previous crm_lib.core imports.

Este módulo expone _norm_key, find_matching_asesor y nuevo_id_cliente que son
utilizados por `crm.py` durante la migración.
"""
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
	"""Busca asesor existente por coincidencia normalizada o devuelve nombre formateado."""
	name = (name or "").strip()
	if not name:
		return ""
	key = _norm_key(name)
	try:
		for a in df.get("asesor", pd.Series()).fillna("").unique():
			if not str(a).strip():
				continue
			if _norm_key(a) == key:
				return a
	except Exception:
		pass
	# Formatear nueva entrada en Title Case
	return " ".join(w.capitalize() for w in name.split())


def nuevo_id_cliente(df: Optional[pd.DataFrame]) -> str:
	"""Genera un nuevo ID tipo 'C<number>' similar a la implementación previa."""
	base_id = 1000
	try:
		if df is not None and not df.empty and "id" in df.columns:
			nums = []
			for x in df["id"].astype(str):
				if not x:
					continue
				if str(x).startswith("C"):
					try:
						nums.append(int(str(x).lstrip("C")))
					except Exception:
						continue
			if nums:
				base_id = max(nums) + 1
			else:
				base_id = base_id + len(df)
	except Exception:
		pass
	return f"C{base_id}"
