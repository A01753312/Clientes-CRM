"""Configuración centralizada del CRM"""
from pathlib import Path
import os

# Paths
BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / "data"
DOCS_DIR = DATA_DIR / "docs"
BACKUPS_DIR = BASE_DIR / "backups"

# Crear directorios necesarios
for dir_path in [DATA_DIR, DOCS_DIR, BACKUPS_DIR]:
    try:
        dir_path.mkdir(parents=True, exist_ok=True)
    except Exception:
        pass

# Archivos principales
CLIENTES_CSV = DATA_DIR / "clientes.csv"
CLIENTES_XLSX = DATA_DIR / "clientes.xlsx"
HISTORIAL_CSV = DATA_DIR / "historial.csv"
USERS_FILE = DATA_DIR / "users.json"

# Catálogos
SUCURSALES_FILE = DATA_DIR / "sucursales.json"
ESTATUS_FILE = DATA_DIR / "estatus.json"
SEGUNDO_ESTATUS_FILE = DATA_DIR / "segundo_estatus.json"

# Google Sheets
USE_GSHEETS = False
GSHEET_ID = ""
GSHEET_TAB = "clientes"
GSHEET_HISTTAB = "historial"
GSHEET_USERSTAB = "users"

# Columnas del DataFrame
COLUMNS = [
    "id", "nombre", "sucursal", "asesor", "fecha_ingreso", 
    "fecha_dispersion", "estatus", "monto_propuesta", "monto_final",
    "segundo_estatus", "observaciones", "score", "telefono", 
    "correo", "analista", "fuente"
]

# Categorías de documentos
DOC_CATEGORIAS = {
    "estado_cuenta": ["pdf", "jpg", "jpeg", "png"],
    "buro_credito": ["pdf", "jpg", "jpeg", "png"],
    "solicitud": ["pdf", "docx", "jpg", "jpeg", "png"],
    "contrato": ["pdf", "docx", "jpg", "jpeg", "png"],
    "otros": ["pdf", "docx", "xlsx", "jpg", "jpeg", "png"],
}

# Permisos por rol
PERMISSIONS = {
    "admin": {"manage_users": True, "delete_client": True},
    "member": {"manage_users": False, "delete_client": False},
}


def load_catalog(file_path: Path, defaults: list) -> list:
    """Carga un catálogo desde JSON o crea con valores por defecto"""
    try:
        if file_path.exists():
            import json
            data = json.loads(file_path.read_text(encoding="utf-8"))
            if isinstance(data, list):
                return [str(x).strip() for x in data if str(x).strip()]
    except Exception:
        pass
    try:
        import json
        file_path.write_text(json.dumps(defaults, ensure_ascii=False, indent=2))
    except Exception:
        pass
    return defaults

# Cargar catálogos
SUCURSALES = load_catalog(SUCURSALES_FILE, ["TOXQUI", "COLOKTE", "KAPITALIZA"])
ESTATUS_OPCIONES = load_catalog(ESTATUS_FILE, [
    "DISPERSADO", "EN ONBOARDING", "PENDIENTE CLIENTE", 
    "PROPUESTA", "PENDIENTE DOC", "REC SOBREENDEUDAMIENTO",
    "REC NO CUMPLE POLITICAS", "REC EDAD"
])
SEGUNDO_ESTATUS_OPCIONES = load_catalog(SEGUNDO_ESTATUS_FILE, [
    "", "DISPERSADO", "EN ONBOARDING", "PEND.ACEPT.CLIENTE",
    "APROB.CON PROPUESTA", "PEND.DOC.PARA EVALUACION",
    "RECH.SOBREENDEUDAMIENTO", "RECH. TIPO PENSION", "RECH.EDAD"
])
