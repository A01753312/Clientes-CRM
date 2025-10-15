from pathlib import Path
from datetime import datetime
import os

# Paths and data dirs (same defaults as original crm.py)
ROOT = Path(".")
DATA_DIR = ROOT / "data"
DATA_DIR.mkdir(parents=True, exist_ok=True)
DOCS_DIR = DATA_DIR / "docs"
DOCS_DIR.mkdir(parents=True, exist_ok=True)
CLIENTES_CSV = DATA_DIR / "clientes.csv"
CLIENTES_XLSX = DATA_DIR / "clientes.xlsx"
BACKUPS_DIR = Path("backups")
BACKUPS_DIR.mkdir(parents=True, exist_ok=True)
HISTORIAL_CSV = DATA_DIR / "historial.csv"
USERS_FILE = DATA_DIR / "users.json"
SUCURSALES_FILE = DATA_DIR / "sucursales.json"
ESTATUS_FILE = DATA_DIR / "estatus.json"
SEGUNDO_ESTATUS_FILE = DATA_DIR / "segundo_estatus.json"

# Google Sheets defaults (can be overridden by crm.py)
USE_GSHEETS = True
GSHEET_ID = "10_xueUKm0O1QwOK1YtZI-dFZlNdKVv82M2z29PfM9qk"
GSHEET_TAB = "clientes"
GSHEET_HISTTAB = "historial"
GSHEET_USERSTAB = "users"

def timestamp_str():
    return datetime.now().strftime("%Y%m%d_%H%M%S")
