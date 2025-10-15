"""Pequeña librería interna para el CRM.

Exporta utilidades compartidas que se han extraído desde `crm.py`.
"""
from .core import _norm_key, find_matching_asesor, nuevo_id_cliente

__all__ = ["_norm_key", "find_matching_asesor", "nuevo_id_cliente"]
