# App para gestión de clientes / CRM
# - Sidebar con filtros/acciones
# - Pestañas ordenadas: Dashboard | Clientes | Documentos | Importar | Historial
# - Auto-refresh tras subir documentos o importar Excel
# - Se ELIMINA la importación de documentos desde ZIP

# === CONFIGURACIÓN PROFESIONAL DEL CRM ===
import streamlit as st
import base64
from datetime import date, datetime
from pathlib import Path

# Configuración de página (DEBE SER LO PRIMERO)
st.set_page_config(
    page_title="KAPITALIZA CRM",
    page_icon="🏢",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://kapitaliza.com/ayuda',
        'Report a bug': 'https://kapitaliza.com/soporte',
        'About': '**KAPITALIZA CRM** v3.0 - Sistema Integral de Gestión de Clientes'
    }
)

# CSS personalizado para look profesional con paleta Kapitaliza
st.markdown("""
<style>
    /* Ocultar el menú de Streamlit y el footer */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Tema oscuro corporativo Kapitaliza */
    .stApp {
        background-color: #1E1E1E;
        color: #FFFFFF;
        font-family: 'Inter', 'Roboto', sans-serif;
    }
    
    /* Estilo del header */
    .stApp header {
        background-color: #2A2A2A;
        border-bottom: 2px solid #3C3C3C;
    }
    
    /* Mejorar tabs con tema Kapitaliza */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background-color: #2A2A2A;
        padding: 10px;
        border-radius: 8px;
        border: 1px solid #3C3C3C;
    }
    
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        padding: 0 24px;
        background-color: #3C3C3C;
        border-radius: 8px;
        border: 2px solid #3C3C3C;
        font-weight: 600;
        color: #BFBFBF;
        transition: all 0.3s ease;
    }
    
    .stTabs [aria-selected="true"] {
        background-color: #FFD41D;
        color: #1E1E1E;
        border-color: #FFD41D;
        box-shadow: 0 2px 8px rgba(255, 212, 29, 0.3);
    }
    
    /* Mejorar métricas con tema Kapitaliza */
    [data-testid="stMetricValue"] {
        font-size: 32px;
        font-weight: 700;
        color: #FFFFFF;
        font-family: 'Poppins', sans-serif;
    }
    
    [data-testid="stMetricLabel"] {
        color: #BFBFBF;
        font-weight: 600;
        font-size: 14px;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    [data-testid="stMetricDelta"] {
        color: #BFBFBF;
        font-weight: 500;
    }
    
    /* Cards para métricas corporativas */
    div[data-testid="metric-container"] {
        background-color: #2A2A2A;
        padding: 20px;
        border-radius: 10px;
        border: 2px solid #3C3C3C;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.4);
        transition: transform 0.3s ease;
    }
    
    div[data-testid="metric-container"]:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 16px rgba(0, 0, 0, 0.5);
    }
    
    /* Dataframes corporativos */
    .dataframe {
        border: 2px solid #3C3C3C;
        border-radius: 10px;
        background-color: #2A2A2A;
        color: #FFFFFF;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.3);
    }
    
    /* Botones corporativos Kapitaliza */
    .stButton > button {
        border-radius: 8px;
        font-weight: 600;
        font-size: 14px;
        transition: all 0.3s ease;
        background-color: #FFD41D;
        color: #1E1E1E;
        border: none;
        padding: 10px 20px;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        box-shadow: 0 2px 8px rgba(255, 212, 29, 0.3);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(255, 212, 29, 0.4);
        background-color: #E6B800;
    }
    
    /* Sidebar corporativo */
    [data-testid="stSidebar"] {
        background-color: #2A2A2A;
        border-right: 2px solid #3C3C3C;
    }
    
    [data-testid="stSidebar"] .css-1d391kg {
        color: #FFFFFF;
    }
    
    /* Expanders corporativos */
    .streamlit-expanderHeader {
        background-color: #3C3C3C;
        border-radius: 8px;
        font-weight: 600;
        color: #FFFFFF;
        border: 1px solid #3C3C3C;
    }
    
    .streamlit-expanderContent {
        background-color: #2A2A2A;
        border: 1px solid #3C3C3C;
        border-radius: 0 0 8px 8px;
    }
    
    /* Inputs corporativos */
    .stTextInput > div > div > input,
    .stSelectbox > div > div > select,
    .stMultiSelect > div > div {
        border-radius: 8px;
        border: 2px solid #3C3C3C;
        background-color: #2A2A2A;
        color: #FFFFFF;
        font-weight: 500;
        transition: border-color 0.3s ease;
    }
    
    .stTextInput > div > div > input:focus,
    .stSelectbox > div > div > select:focus {
        border-color: #FFD41D;
        box-shadow: 0 0 0 2px rgba(255, 212, 29, 0.2);
    }
    
    /* Spinner corporativo */
    .stSpinner > div {
        border-top-color: #FFD41D !important;
    }
    
    /* Títulos y encabezados */
    h1, h2, h3 {
        color: #FFFFFF;
        font-family: 'Poppins', sans-serif;
        font-weight: 700;
    }
    
    h1 {
        font-size: 2.5rem;
    }
    
    h2 {
        font-size: 2rem;
    }
    
    h3 {
        font-size: 1.5rem;
    }
    
    /* Texto secundario */
    .stMarkdown p, .stText {
        color: #BFBFBF;
        line-height: 1.6;
    }
    
    /* Info boxes con colores corporativos */
    .stAlert[data-baseweb="notification"] {
        background-color: #2A2A2A;
        border: 2px solid #3C3C3C;
        border-radius: 8px;
        color: #FFFFFF;
    }
    
    /* Success (Verde suave) */
    .stSuccess {
        background-color: #2A2A2A;
        border-left: 4px solid #4CAF50;
        color: #FFFFFF;
    }
    
    /* Error (Rojo profesional) */
    .stError {
        background-color: #2A2A2A;
        border-left: 4px solid #D9534F;
        color: #FFFFFF;
    }
    
    /* Warning */
    .stWarning {
        background-color: #2A2A2A;
        border-left: 4px solid #FFD41D;
        color: #FFFFFF;
    }
    
    /* Info */
    .stInfo {
        background-color: #2A2A2A;
        border-left: 4px solid #3C3C3C;
        color: #FFFFFF;
    }
    
    /* Selectbox dropdown corporativo */
    .stSelectbox > div > div > div {
        background-color: #2A2A2A;
        color: #FFFFFF;
        border: 1px solid #3C3C3C;
        border-radius: 8px;
    }
    
    /* Multiselect corporativo */
    .stMultiSelect > div > div > div {
        background-color: #2A2A2A;
        color: #FFFFFF;
        border: 1px solid #3C3C3C;
        border-radius: 8px;
    }
    
    /* Radio buttons */
    .stRadio > div > label {
        color: #FFFFFF;
        font-weight: 500;
    }
    
    /* Checkbox */
    .stCheckbox > label {
        color: #FFFFFF;
        font-weight: 500;
    }
    
    /* Toast messages */
    .stToast {
        background-color: #2A2A2A;
        color: #FFFFFF;
        border: 1px solid #3C3C3C;
        border-radius: 8px;
    }
    
    /* Progress bar */
    .stProgress > div > div {
        background-color: #FFD41D;
    }
    
    /* Caption text */
    .css-1v0mbdj {
        color: #BFBFBF;
        font-size: 12px;
    }
</style>
""", unsafe_allow_html=True)

import io
import re
import json
import zipfile  # (aún se usa para exportar ZIPs, no para importar)  # CHANGED: seguimos exportando
import os
import hashlib
import secrets
import difflib
import unicodedata
import time

import pandas as pd
import gspread
from gspread_dataframe import get_as_dataframe, set_with_dataframe
from google.oauth2.service_account import Credentials
import shutil
import altair as alt
from google.auth.transport.requests import Request

# Debug info removed by user request (sidebar debug block intentionally deleted)

# === FUNCIONES PROFESIONALES DEL CRM ===

# Función para mostrar loading personalizado
def show_loading(message="Procesando..."):
    """Muestra un loading spinner más profesional"""
    return st.spinner(f"⚙️ {message}")

# Función para notificaciones más profesionales
def show_notification(message: str, type: str = "success"):
    """
    Muestra notificaciones profesionales
    type: 'success', 'info', 'warning', 'error'
    """
    icons = {
        "success": "✅",
        "info": "ℹ️",
        "warning": "⚠️",
        "error": "❌"
    }
    
    icon = icons.get(type, "ℹ️")
    
    # Usar toast para notificaciones no intrusivas
    try:
        st.toast(f"{icon} {message}", icon=icon)
    except:
        # Fallback si toast no está disponible
        if type == "success":
            st.success(f"{icon} {message}")
        elif type == "error":
            st.error(f"{icon} {message}")
        elif type == "warning":
            st.warning(f"{icon} {message}")
        else:
            st.info(f"{icon} {message}")

# Funciones de feedback mejorado
def show_success(message, duration=3):
    """Muestra mensaje de éxito usando componentes nativos de Streamlit"""
    st.toast(f"✅ {message}", icon="✅")
    st.success(f"✅ {message}")

def show_error(message):
    """Muestra mensaje de error usando componentes nativos de Streamlit"""
    st.toast(f"❌ {message}", icon="❌")
    st.error(f"❌ {message}")

def show_warning(message):
    """Muestra advertencia usando componentes nativos de Streamlit"""
    st.toast(f"⚠️ {message}", icon="⚠️")
    st.warning(f"⚠️ {message}")

def show_info(message):
    """Muestra información usando componentes nativos de Streamlit"""
    st.toast(f"ℹ️ {message}", icon="ℹ️")
    st.info(f"ℹ️ {message}")

# Cards profesionales para KPIs
def render_kpi_card(label: str, value: any, delta: str = None, icon: str = "📊", color: str = "#0066cc"):
    """Renderiza una tarjeta KPI profesional"""
    delta_html = ""
    if delta:
        delta_color = "#28a745" if "+" in str(delta) or "↑" in str(delta) else "#dc3545"
        delta_html = f'<p style="color: {delta_color}; margin: 5px 0 0 0; font-size: 14px; font-weight: 500;">{delta}</p>'
    
    card_html = f"""
    <div style="
        background: white;
        padding: 20px;
        border-radius: 12px;
        border-left: 4px solid {color};
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        margin-bottom: 10px;
        height: 140px;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
    ">
        <div style="display: flex; justify-content: space-between; align-items: flex-start;">
            <div style="flex: 1;">
                <p style="color: #6c757d; margin: 0; font-size: 14px; font-weight: 500; text-transform: uppercase; letter-spacing: 0.5px;">
                    {label}
                </p>
                <h2 style="color: #212529; margin: 10px 0 0 0; font-size: 32px; font-weight: 700; line-height: 1;">
                    {value}
                </h2>
            </div>
            <div style="font-size: 32px; opacity: 0.4; margin-left: 15px;">
                {icon}
            </div>
        </div>
        {delta_html}
    </div>
    """
    st.markdown(card_html, unsafe_allow_html=True)

def get_base64_image(image_path):
    """Convierte imagen a base64 para embedding en HTML"""
    import base64
    with open(image_path, "rb") as f:
        return base64.b64encode(f.read()).decode()

# Header profesional simplificado
def render_professional_header():
    """Renderiza un header profesional corporativo usando componentes nativos de Streamlit"""
    u = current_user()
    user_name = u.get('user') or u.get('email') if u else "Usuario"
    current_time = datetime.now().strftime("%d/%m/%Y %H:%M")
    
    # Usar columnas para el layout del header
    col1, col2, col3 = st.columns([1, 3, 1])
    
    with col2:
        st.markdown("""
        <div style="text-align: center; padding: 20px; margin-bottom: 20px;">
            <h1 style="color: #FFD41D; font-size: 3rem; margin: 0; font-weight: 700;">
                🏢 KAPITALIZA CRM
            </h1>
            <p style="color: #BFBFBF; font-size: 1.1rem; margin: 10px 0 0 0;">
                Sistema Integral de Gestión de Clientes
            </p>
            <p style="color: #3C3C3C; font-size: 0.9rem; margin: 5px 0 0 0;">
                {user_name} | {current_time}
            </p>
        </div>
        """.format(user_name=user_name, current_time=current_time), unsafe_allow_html=True)
    
    # Línea separadora dorada
    st.markdown("""
    <hr style="
        border: none; 
        height: 3px; 
        background: linear-gradient(90deg, #FFD41D 0%, #E6B800 100%);
        margin: 0 0 30px 0;
        border-radius: 2px;
    ">
    """, unsafe_allow_html=True)

def run_with_progress(func, steps: list, *args, **kwargs):
    """Ejecuta función con barra de progreso"""
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    total_steps = len(steps)
    for i, step in enumerate(steps):
        progress = (i + 1) / total_steps
        progress_bar.progress(progress)
        status_text.text(f"⚙️ {step}...")
        
    result = func(*args, **kwargs)
    
    progress_bar.progress(1.0)
    status_text.text("✅ Completado!")
    time.sleep(0.5)
    progress_bar.empty()
    status_text.empty()
    
    return result

# Paths and data dirs
DATA_DIR = Path("data")
DATA_DIR.mkdir(parents=True, exist_ok=True)
DOCS_DIR = DATA_DIR / "docs"
DOCS_DIR.mkdir(parents=True, exist_ok=True)
CLIENTES_CSV = DATA_DIR / "clientes.csv"
CLIENTES_XLSX = DATA_DIR / "clientes.xlsx"

# === CONFIGURACIÓN GOOGLE SHEETS ===
USE_GSHEETS = True   # pon False si quieres trabajar sólo local
GSHEET_ID      = "10_xueUKm0O1QwOK1YtZI-dFZlNdKVv82M2z29PfM9qk"
GSHEET_TAB     = "clientes"    # tu pestaña principal
GSHEET_HISTTAB = "historial"   # tu pestaña de historial


# Opcional: pega aquí el contenido JSON del service account si prefieres no usar el archivo
# Si la variable está vacía (""), se seguirá leyendo `service_account.json` desde disco.
SERVICE_ACCOUNT_JSON_STR = ""
# CACHING para gspread: minimizar auth / apertura repetida durante reruns
_GS_CREDS = None
_GS_GC = None
_GS_SH = None
_GS_WS_CACHE: dict = {}

def _gs_credentials():
    """Carga credenciales desde Streamlit secrets - Versión mejorada para Streamlit Cloud"""
    global _GS_CREDS
    if _GS_CREDS is not None:
        return _GS_CREDS
    try:
        # 1) Streamlit Secrets (PRIMARIO para Streamlit Cloud)
        if hasattr(st, "secrets"):
            secrets_dict = dict(st.secrets)
            
            # Buscar en diferentes estructuras posibles
            sa_info = None
            
            # Opción 1: Secrets directamente en el nivel raíz
            if all(k in secrets_dict for k in ["type", "project_id", "private_key_id", "private_key"]):
                sa_info = secrets_dict
            # Opción 2: Dentro de key 'service_account'
            elif 'service_account' in secrets_dict:
                sa_info = dict(secrets_dict['service_account'])
            
            if sa_info:
                # Asegurar que la private_key tenga los saltos de línea correctos
                if "private_key" in sa_info:
                    sa_info["private_key"] = sa_info["private_key"].replace("\\n", "\n")
                
                scopes = ["https://www.googleapis.com/auth/spreadsheets"]
                _GS_CREDS = Credentials.from_service_account_info(sa_info, scopes=scopes)
                return _GS_CREDS
        
        # 2) Fallback para desarrollo local
        try:
            with open("service_account.json", "r", encoding="utf-8") as f:
                import json
                sa_info = json.load(f)
                if "private_key" in sa_info:
                    sa_info["private_key"] = sa_info["private_key"].replace("\\n", "\n")
                scopes = ["https://www.googleapis.com/auth/spreadsheets"]
                _GS_CREDS = Credentials.from_service_account_info(sa_info, scopes=scopes)
                return _GS_CREDS
        except FileNotFoundError:
            pass
            
        st.error("❌ No se pudieron cargar las credenciales de Google Sheets")
        return None
        
    except Exception as e:
        st.error(f"❌ Error en autenticación Google Sheets: {str(e)}")
        return None

def _gs_open_worksheet(tab_name: str):
    """Versión silenciosa: Abre una pestaña, pero no muestra mensajes en la UI después del primer render.
    Devuelve None en caso de cualquier problema (silencioso)."""
    global _GS_GC, _GS_SH, _GS_WS_CACHE
    try:
        if tab_name in _GS_WS_CACHE:
            return _GS_WS_CACHE[tab_name]

        creds = _gs_credentials()
        if creds is None:
            return None

        if _GS_GC is None:
            _GS_GC = gspread.authorize(creds)
        
        if _GS_SH is None:
            try:
                _GS_SH = _GS_GC.open_by_key(GSHEET_ID)
                # silencioso: no mostrar mensajes en UI
            except Exception:
                return None

        try:
            ws = _GS_SH.worksheet(tab_name)
        except gspread.exceptions.WorksheetNotFound:
            ws = _GS_SH.add_worksheet(title=tab_name, rows="5000", cols="50")
            # silencioso: no mostrar información al usuario

        _GS_WS_CACHE[tab_name] = ws
        return ws
        
    except Exception:
        return None

def limpiar_cache_gsheets():
    """Limpia todos los cachés de Google Sheets para forzar recarga de datos."""
    global _GS_GC, _GS_SH, _GS_WS_CACHE
    _GS_WS_CACHE.clear()
    _GS_GC = None
    _GS_SH = None
    # También limpiar caché de Streamlit
    st.cache_data.clear()
    # Limpiar flags de session_state relacionados con la carga
    if 'gs_load_msg_shown' in st.session_state:
        del st.session_state['gs_load_msg_shown']

def find_logo_path() -> Path | None:
    # Buscar logo en data/ (logo.png, logo.jpg) o en data/logo subfolder
    candidates = [DATA_DIR / "logo.png", DATA_DIR / "logo.jpg", DATA_DIR / "logo.jpeg"]
    for p in candidates:
        if p.exists():
            return p
    # buscar en carpeta docs o raíz
    altp = DATA_DIR / "logo.png"
    if altp.exists():
        return altp
    return None

SUCURSALES_FILE = DATA_DIR / "sucursales.json"

def load_sucursales() -> list:
    """
    Carga la lista de sucursales desde un JSON en DATA_DIR. Si no existe, crea el archivo con valores por defecto.
    """
    try:
        if SUCURSALES_FILE.exists():
            data = json.loads(SUCURSALES_FILE.read_text(encoding="utf-8"))
            if isinstance(data, list):
                # Normalizar a strings y limpiar
                return [str(x).strip() for x in data if str(x).strip()]
    except Exception:
        pass
    # Valores por defecto
    defaults = ["TOXQUI", "COLOKTE", "KAPITALIZA"]
    try:
        SUCURSALES_FILE.write_text(json.dumps(defaults, ensure_ascii=False, indent=2), encoding="utf-8")
    except Exception:
        pass
    return defaults

def save_sucursales(lst: list):
    try:
        clean = [str(x).strip() for x in lst if str(x).strip()]
        SUCURSALES_FILE.write_text(json.dumps(clean, ensure_ascii=False, indent=2), encoding="utf-8")
    except Exception:
        pass

# Inicializar lista de sucursales desde disco
SUCURSALES = load_sucursales()
ESTATUS_FILE = DATA_DIR / "estatus.json"
SEGUNDO_ESTATUS_FILE = DATA_DIR / "segundo_estatus.json"

def load_estatus() -> list:
    defaults = ["DISPERSADO","EN ONBOARDING","PENDIENTE CLIENTE","PROPUESTA","PENDIENTE DOC","REC SOBREENDEUDAMIENTO","REC NO CUMPLE POLITICAS","REC EDAD"]
    try:
        if ESTATUS_FILE.exists():
            data = json.loads(ESTATUS_FILE.read_text(encoding="utf-8"))
            if isinstance(data, list):
                return [str(x).strip() for x in data if str(x).strip()]
    except Exception:
        pass
    try:
        ESTATUS_FILE.write_text(json.dumps(defaults, ensure_ascii=False, indent=2), encoding="utf-8")
    except Exception:
        pass
    return defaults

def save_estatus(lst: list):
    try:
        clean = [str(x).strip() for x in lst if str(x).strip()]
        ESTATUS_FILE.write_text(json.dumps(clean, ensure_ascii=False, indent=2), encoding="utf-8")
    except Exception:
        pass

def load_segundo_estatus() -> list:
    defaults = ["","DISPERSADO","EN ONBOARDING","PEND.ACEPT.CLIENTE","APROB.CON PROPUESTA","PEND.DOC.PARA EVALUACION","RECH.SOBREENDEUDAMIENTO","RECH. TIPO PENSION","RECH.EDAD"]
    try:
        if SEGUNDO_ESTATUS_FILE.exists():
            data = json.loads(SEGUNDO_ESTATUS_FILE.read_text(encoding="utf-8"))
            if isinstance(data, list):
                return [str(x).strip() for x in data if str(x).strip() or x == ""]
    except Exception:
        pass
    try:
        SEGUNDO_ESTATUS_FILE.write_text(json.dumps(defaults, ensure_ascii=False, indent=2), encoding="utf-8")
    except Exception:
        pass
    return defaults

def save_segundo_estatus(lst: list):
    try:
        clean = [str(x).strip() for x in lst if (str(x).strip() or x == "")]
        SEGUNDO_ESTATUS_FILE.write_text(json.dumps(clean, ensure_ascii=False, indent=2), encoding="utf-8")
    except Exception:
        pass

# Inicializar catálogos desde disco
ESTATUS_OPCIONES = load_estatus()
SEGUNDO_ESTATUS_OPCIONES = load_segundo_estatus()

DOC_CATEGORIAS = {
    "estado_cuenta": ["pdf", "jpg", "jpeg", "png"],
    "buro_credito":  ["pdf", "jpg", "jpeg", "png"],
    "solicitud":     ["pdf", "docx", "jpg", "jpeg", "png"],
    "contrato":      ["pdf", "docx", "jpg", "jpeg", "png"],  # visible si estatus = en dispersión
    "otros":         ["pdf", "docx", "xlsx", "jpg", "jpeg", "png"],
}

# ---------- Helpers ----------
SAFE_NAME_RE = re.compile(r"[^A-Za-z0-9._\\-áéíóúÁÉÍÓÚñÑ ]+")

def sort_df_by_dates(df: pd.DataFrame) -> pd.DataFrame:
    """
    Ordena el DataFrame por las columnas de fecha si existen ('fecha_ingreso', 'fecha_dispersion', 'ts').
    Si ninguna existe, retorna el DataFrame sin cambios.
    """
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

def safe_name(s: str) -> str:
    if s is None:
        return ""
    s = str(s).strip()
    s = SAFE_NAME_RE.sub("_", s)
    s = re.sub(r"\s+", " ", s)
    return s[:150]

# NEW: normalización y búsqueda de asesor existente
def _norm_key(s: str) -> str:
    s = (s or "")
    s = str(s).strip()
    s = re.sub(r"\s+", " ", s)
    s = unicodedata.normalize("NFKD", s)
    s = "".join(ch for ch in s if not unicodedata.combining(ch))
    # usar casefold() en lugar de lower() para una comparación Unicode más robusta
    return s.casefold()

def find_matching_asesor(name: str, df: pd.DataFrame) -> str:
    """
    Si name coincide (normalizado) con algún 'asesor' ya presente en df -> retorna la forma registrada.
    Si no hay coincidencia, retorna name limpio con capitalización de palabras (o '' si vacío).
    """
    name = (name or "").strip()
    if not name:
        return ""
    name_key = _norm_key(name)
    # buscar en el dataframe por la clave normalizada
    for a in df["asesor"].fillna("").unique():
        if not str(a).strip():
            continue
        if _norm_key(a) == name_key:
            return a  # usar la forma ya existente
    # si no existe, devolver una versión "limpia" con Title Case (mínima transformación)
    return " ".join(w.capitalize() for w in name.split())


# ----- Document helpers para manejo de archivos de clientes -----
def carpeta_docs_cliente(cid: str) -> Path:
    """
    Retorna la carpeta donde se almacenan los documentos para el cliente `cid`.
    Crea la carpeta si no existe.
    """
    # Preferir usar el nombre del cliente como carpeta (más legible).
    # Si no hay nombre, o no se encuentra, fallback al id.
    try:
        nombre = get_nombre_by_id(cid) or ""
    except Exception:
        nombre = ""

    name_safe = safe_name(nombre) if nombre else ""
    id_safe = safe_name(str(cid))

    # Si hay un nombre válido, usar/crear esa carpeta. Si existe la carpeta por id,
    # intentar migrar su contenido a la carpeta por nombre para conservar documentos.
    if name_safe:
        name_folder = DOCS_DIR / name_safe
        id_folder = DOCS_DIR / id_safe
        try:
            if id_folder.exists() and id_folder.is_dir() and not name_folder.exists():
                # mover la carpeta entera para preservar archivos previos
                shutil.move(str(id_folder), str(name_folder))
        except Exception:
            # si la migración falla, no bloquear: seguiremos usando/creando name_folder
            pass
        folder = name_folder
    else:
        folder = DOCS_DIR / id_safe

    folder.mkdir(parents=True, exist_ok=True)
    return folder

def canonicalize_from_catalog(
    raw: str,
    catalog: list[str],
    extra_synonyms: dict[str, str] | None = None,
    min_ratio: float = 0.90
) -> str:
    """
    Devuelve el valor 'raw' mapeado al elemento 'canónico' del catálogo más similar:
    - Igualdad exacta tras normalizar (ignora acentos/case/espacios)
    - Sinónimos explícitos (opcional)
    - 'Fuzzy' por similitud (difflib) con umbral min_ratio
    Si no encuentra nada suficientemente parecido → devuelve 'raw' tal cual.
    """
    s = (raw or "").strip()
    if not s:
        return s

    key = _norm_key(s)

    # 1) match exacto normalizado
    for opt in catalog:
        if _norm_key(opt) == key:
            return opt

    # 2) sinónimos opcionales (mapa: "en revision" -> "EN REVISIÓN")
    if extra_synonyms:
        for k, v in extra_synonyms.items():
            if _norm_key(k) == key:
                # devolver el canónico si existe en catálogo; si no, el sinónimo
                for opt in catalog:
                    if _norm_key(opt) == _norm_key(v):
                        return opt
                return v

    # 3) fuzzy: el más parecido por ratio
    best, best_r = None, 0.0
    for opt in catalog:
        r = difflib.SequenceMatcher(None, key, _norm_key(opt)).ratio()
        if r > best_r:
            best_r, best = r, opt

    if best and best_r >= min_ratio:
        return best

    return s


def subir_docs(cid: str, files, prefijo: str = "") -> list:
    """
    Guarda una lista de archivos subidos por Streamlit en la carpeta del cliente.
    `files` puede ser una lista de UploadedFile o similar; cada objeto debe exponer `.name` y `.read()` / `.getbuffer()`.
    `prefijo` se antepone al nombre del archivo en disco.
    NO escribe en historial; retorna la lista de nombres guardados.
    """
    if not cid:
        return []
    folder = carpeta_docs_cliente(cid)
    # Asegurar que `files` sea iterable (Streamlit acepta single file o lista)
    if files is None:
        return []
    files_iter = files if hasattr(files, '__iter__') and not isinstance(files, (bytes, bytearray)) else [files]

    # Primero: leer todo el contenido en memoria de forma segura
    to_write = []  # list of tuples (target_name, bytes)
    for f in files_iter:
        try:
            fname = getattr(f, "name", None) or getattr(f, "filename", None) or "uploaded"
            target_name = safe_name(f"{prefijo}{fname}")
            data = None
            if hasattr(f, "getbuffer"):
                try:
                    data = f.getbuffer()
                except Exception:
                    data = None
            if data is None and hasattr(f, "read"):
                try:
                    data = f.read()
                except Exception:
                    data = None
            if data is None:
                continue
            if isinstance(data, memoryview):
                data = data.tobytes()
            # ensure bytes
            if isinstance(data, str):
                data = data.encode("utf-8")
            if not isinstance(data, (bytes, bytearray)):
                try:
                    data = bytes(data)
                except Exception:
                    continue
            to_write.append((target_name, data))
        except Exception:
            continue

    # Escribir en paralelo para acelerar (especialmente cuando hay varios archivos)
    saved_files = []
    try:
        import concurrent.futures
        max_workers = min(4, (len(to_write) or 1))
        def _write_item(item):
            tname, b = item
            try:
                out_path = folder / tname
                out_path.write_bytes(b)
                return tname
            except Exception:
                return None

        with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as ex:
            futures = [ex.submit(_write_item, it) for it in to_write]
            for fut in concurrent.futures.as_completed(futures):
                try:
                    res = fut.result()
                    if res:
                        saved_files.append(res)
                except Exception:
                    continue
    except Exception:
        # fallback a escritura secuencial si algo falla
        for tname, b in to_write:
            try:
                out_path = folder / tname
                out_path.write_bytes(b)
                saved_files.append(tname)
            except Exception:
                continue
    # devolver la lista de archivos guardados para que el llamador registre 1 entrada por lote
    return saved_files


def listar_docs_cliente(cid: str):
    """
    Lista los archivos asociados a un cliente (Path objects), ordenados por nombre.
    Retorna lista vacía si no existe carpeta.
    """
    try:
        nombre = get_nombre_by_id(cid) or ""
    except Exception:
        nombre = ""

    name_safe = safe_name(nombre) if nombre else ""
    id_safe = safe_name(str(cid))

    # Preferir la carpeta por nombre si existe; si no, revisar la carpeta por id.
    if name_safe:
        folder = DOCS_DIR / name_safe
        if folder.exists() and folder.is_dir():
            return sorted([p for p in folder.iterdir() if p.is_file()], key=lambda p: p.name)

    folder_id = DOCS_DIR / id_safe
    if folder_id.exists() and folder_id.is_dir():
        return sorted([p for p in folder_id.iterdir() if p.is_file()], key=lambda p: p.name)

    return []


def nuevo_id_cliente(df: pd.DataFrame) -> str:
    """
    Genera un nuevo ID de cliente único con prefijo 'C' basado en los IDs existentes del DataFrame.
    Si no encuentra IDs del formato C<number>, comienza en C1000.
    """
    base_id = 1000
    try:
        if df is not None and not df.empty and "id" in df.columns:
            nums = []
            for x in df["id"].astype(str):
                if not x:
                    continue
                m = re.match(r"^C(\d+)$", str(x).strip())
                if m:
                    try:
                        nums.append(int(m.group(1)))
                    except Exception:
                        continue
            if nums:
                base_id = max(nums) + 1
            else:
                # fallback: avoid collision con filas existentes
                base_id = base_id + len(df)
    except Exception:
        base_id = base_id
    return f"C{base_id}"

def get_nombre_by_id(cid: str) -> str:
    """Retorna el nombre del cliente por id de forma segura ('' si no existe)."""
    try:
        if cid is None or cid == "":
            return ""
        if 'id' not in df_cli.columns or df_cli.empty:
            return ""
        sel = df_cli.loc[df_cli['id'] == cid, 'nombre']
        if sel is None or sel.empty:
            return ""
        return str(sel.values[0])
    except Exception:
        return ""

def get_field_by_id(cid: str, field: str) -> str:
    """Retorna el valor de `field` para el cliente `cid` de forma segura ('' si no existe)."""
    try:
        if cid is None or cid == "":
            return ""
        if 'id' not in df_cli.columns or df_cli.empty:
            return ""
        if field not in df_cli.columns:
            return ""
        sel = df_cli.loc[df_cli['id'] == cid, field]
        if sel is None or sel.empty:
            return ""
        return str(sel.values[0])
    except Exception:
        return ""

# --- NEW: búsquedas rápidas y cacheadas (preindexado) ---
@st.cache_data(show_spinner=False)
def build_text_index(options: list[str]):
	opts = [str(o) for o in options]
	norms = [_norm_key(o) for o in opts]
	tokens = [set(n.split()) for n in norms]
	inv = {}
	for i, toks in enumerate(tokens):
		for t in toks:
			inv.setdefault(t, set()).add(i)
	initials = ["".join(w[0] for w in n.split() if w) for n in norms]
	buckets = {}
	for i, n in enumerate(norms):
		b = n[:1]
		buckets.setdefault(b, []).append(i)
	return {"opts": opts, "norms": norms, "tokens": tokens, "inv": inv, "initials": initials, "buckets": buckets}

import re as _re

# --- ROBUST SEARCH (reemplaza fast_search) ---
def _parse_query(q: str):
    """
    Soporta:
      - AND por espacios
      - OR por comas (cada parte es un grupo AND)
      - Frases exactas entre "comillas"
      - Exclusiones con -token o !token
      - Prefijos con asterisco: vent*  (== "empieza por vent")
    """
    q = (q or "").strip()
    if not q:
        return []

    parts = [p.strip() for p in q.split(",") if p.strip()]  # OR
    groups = []
    for part in parts:
        phrases = [_norm_key(m) for m in _re.findall(r'"([^"]+)"', part)]
        base = _re.sub(r'"[^"]+"', " ", part)

        req, excl = [], []
        for t in [t for t in _re.split(r"\s+", base) if t]:
            neg = t.startswith("-") or t.startswith("!")
            tt = t[1:] if neg else t
            tt = _norm_key(tt)
            if not tt:
                continue
            (excl if neg else req).append(tt)

        groups.append({"req": req, "phrases": phrases, "exclude": excl})
    return groups

def _score_match(opt_norm: str, opt_tokens: set[str], opt_initials: str, group: dict) -> tuple[bool, float]:
    # exclusiones
    for ex in group["exclude"]:
        ex_base = ex.rstrip("*")
        if any(t.startswith(ex_base) for t in opt_tokens) or ex_base in opt_norm:
            return False, 0.0

    score = 0.0

    # frases exactas (todas)
    for ph in group["phrases"]:
        if ph in opt_norm:
            score += 3.0
        else:
            return False, 0.0

    # requisitos (todas)
    for req in group["req"]:
        is_prefix = req.endswith("*")
        base = req.rstrip("*")
        hit = False

        if base in opt_tokens:                       # token exacto
            score += 2.0; hit = True
        elif any(t.startswith(base) for t in opt_tokens):  # prefijo
            score += 1.6 if is_prefix else 1.4; hit = True
        elif base in opt_norm:                       # substring
            score += 1.2; hit = True
        elif opt_initials.startswith(base):          # iniciales
            score += 1.0; hit = True
        else:
            # fuzzy contra todo el texto normalizado (tolerancia a typos)
            ratio = difflib.SequenceMatcher(None, base, opt_norm).ratio()
            if ratio >= 0.82:
                score += 0.8; hit = True

        if not hit:
            return False, 0.0

    return True, score

def robust_search(q: str, idx: dict, limit: int | None = None) -> list[str]:
    """
    Búsqueda determinista y tolerante:
      - AND (espacios), OR (comas), "frases", -exclusiones, prefijo*
      - Acentos/case ignorados · fuzzy para typos
      - Fallback seguro si no hay matches
    """
    if not q:
        return idx["opts"]

    groups = _parse_query(q)
    if not groups:
        return idx["opts"]

    scored = []
    for i, opt_norm in enumerate(idx["norms"]):
        ok_any = False
        best = 0.0
        for g in groups:
            matched, sc = _score_match(opt_norm, idx["tokens"][i], idx["initials"][i], g)
            if matched:
                ok_any = True
                best = max(best, sc)
        if ok_any:
            best += min(0.5, len(idx["opts"][i]) / 200.0)  # bonus pequeño estable
            scored.append((best, i))

    if not scored:
        # fallback: similitud global contra la query (normalizada)
        q_norm = _norm_key(_re.sub(r'"', "", q))
        pool = idx["norms"]
        close = difflib.get_close_matches(q_norm, pool, n=min(12, len(pool)), cutoff=0.6)
        ids = []
        for val in close:
            try:
                ids.append(pool.index(val))
            except ValueError:
                pass
        out = [idx["opts"][j] for j in ids] or idx["opts"]
        return out[:limit] if limit else out

    scored.sort(key=lambda x: (-x[0], x[1]))
    out = [idx["opts"][i] for _, i in scored]
    return out[:limit] if limit else out

# --- /ROBUST SEARCH ---


def stable_multiselect(
    *,
    title: str,
    idx: dict,
    state_key: str,
    search_key: str,
    help_txt: str,
    all_options: list[str],
    on_all,
    on_none,
    min_len: int = 1,
    display_inline: bool = False,
):
    """
    Multiselect estable con popover/expander:
      - Estado lógico en st.session_state[state_key]
      - Estado visual del widget en st.session_state[w_<state_key>]
      - Botones: Todos / Ninguno / Añadir / Reemplazar / Limpiar / Nueva búsqueda
      - Sincronización widget ← estado en acciones para evitar que el widget pise tu selección.
    """
    # Contenedor
    # Contenedor: por defecto popover/expander, pero si display_inline==True renderizamos directo en sidebar
    if display_inline:
        pop = st.sidebar
    else:
        try:
            pop = st.sidebar.popover(f"{title} · {len(st.session_state.get(state_key, []))}/{len(all_options)}")
        except Exception:
            pop = st.sidebar.expander(f"{title} · {len(st.session_state.get(state_key, []))}/{len(all_options)}", expanded=False)

    # Safety: ensure `pop` is a Streamlit container (DeltaGenerator-like); fallback if not
    try:
        if not hasattr(pop, "fragment_id_queue"):
            pop = st.sidebar.expander(f"{title} · {len(st.session_state.get(state_key, []))}/{len(all_options)}", expanded=False)
    except Exception:
        try:
            pop = st.sidebar.expander(f"{title} · {len(st.session_state.get(state_key, []))}/{len(all_options)}", expanded=False)
        except Exception:
            pop = st.sidebar

    # Estado lógico inicial (una sola vez)
    st.session_state.setdefault(state_key, [o for o in all_options])

    # Widget key separado
    wkey = f"w_{state_key}"
    chk_key = f"{state_key}_all_chk"

    def _set_all():
        st.session_state[state_key] = [o for o in all_options]
        try:
            on_all()
        except Exception:
            pass

    def _set_none():
        st.session_state[state_key] = []
        try:
            on_none()
        except Exception:
            pass

    with pop:
        # Checkbox 'Todas' que determina si está todo seleccionado
        is_now_all = set(st.session_state.get(state_key, [])) == set(all_options)
        if chk_key in st.session_state:
            checked = st.checkbox("Todas", key=chk_key)
        else:
            st.session_state.setdefault(chk_key, is_now_all)
            checked = st.checkbox("Todas", value=is_now_all, key=chk_key)

        # Si el checkbox cambió, actualizar estado lógico
        if checked and not is_now_all:
            _set_all()
        elif (not checked) and is_now_all:
            _set_none()

        # Mostrar multiselect desplegado (sin buscador ni botones)
        opts = [o for o in all_options]
        selected_now = [o for o in st.session_state.get(state_key, []) if o in all_options]
        if wkey in st.session_state:
            sel = st.multiselect("", options=opts, key=wkey, label_visibility="collapsed", help=help_txt)
        else:
            sel = st.multiselect("", options=opts, default=selected_now, key=wkey, label_visibility="collapsed", help=help_txt)

        # Sincronizar widget → estado lógico
        if sel != st.session_state.get(state_key):
            st.session_state[state_key] = [o for o in sel if o in all_options]
            # sincronizar checkbox
            st.session_state[chk_key] = (set(st.session_state[state_key]) == set(all_options))

def _is_dispersion(estatus: str) -> bool:
    e = _norm_key(estatus)
    return e in {_norm_key("DISPERSADO"), _norm_key("EN DISPERSIÓN"), _norm_key("EN DISPERSION")}

# === Helper: multiselección con estética de selectbox ===
# ...existing code...
def selectbox_multi(label: str, options: list[str], state_key: str) -> list[str]:
    opts = [str(o) for o in options]
    opts = list(dict.fromkeys(opts))

    st.session_state.setdefault(state_key, opts.copy())
    selected = [o for o in st.session_state[state_key] if o in opts]
    all_selected = (set(selected) == set(opts))

    # usar popover del sidebar para mejor comportamiento de reruns
    try:
        pop = st.sidebar.popover(label)
    except Exception:
        pop = st.sidebar.expander(label, expanded=False)

    # Safety: if pop is not a Streamlit container (unexpected), fallback to expander or sidebar
    try:
        if not hasattr(pop, "fragment_id_queue"):
            pop = st.sidebar.expander(label, expanded=False)
    except Exception:
        try:
            pop = st.sidebar.expander(label, expanded=False)
        except Exception:
            pop = st.sidebar

    wkey = f"{state_key}_ms"
    chk_key = f"{state_key}_all"

    def _on_checkbox():
        if st.session_state.get(chk_key):
            st.session_state[state_key] = opts.copy()
            st.session_state[wkey] = opts.copy()
        else:
            st.session_state[state_key] = []
            st.session_state[wkey] = []
        st.session_state["_filters_token"] = st.session_state.get("_filters_token", 0) + 1

    def _on_ms_change():
        st.session_state[state_key] = [o for o in st.session_state.get(wkey, []) if o in opts]
        st.session_state[chk_key] = set(st.session_state[state_key]) == set(opts)
        st.session_state["_filters_token"] = st.session_state.get("_filters_token", 0) + 1

    with pop:
        # encabezado resumido
        c1, c2 = st.columns([0.85, 0.15])
        with c1:
            st.caption(label)
            if set(st.session_state.get(state_key, [])) == set(opts):
                st.write("(Todas)")
            elif not st.session_state.get(state_key):
                st.write("— Ninguna —")
            elif len(st.session_state.get(state_key, [])) <= 3:
                st.write(", ".join(st.session_state.get(state_key, [])))
            else:
                st.write(f"{len(st.session_state.get(state_key, []))} seleccionadas")
        with c2:
            st.write("")  # espacio para el botón pequeño

        checked = st.checkbox("Seleccionar todas", value=all_selected, key=chk_key, on_change=_on_checkbox)
        # multiselect con callback para sincronizar y forzar rerun
        if checked:
            st.multiselect("", options=opts, default=opts, disabled=True, label_visibility="collapsed", key=wkey)
        else:
            st.multiselect("", options=opts, default=selected, label_visibility="collapsed", key=wkey, on_change=_on_ms_change)

    return st.session_state[state_key]

# ---------- Sidebar (filtros + acciones) ----------
# Columnas esperadas en el CSV / DataFrame de clientes
COLUMNS = [
    "id","nombre","sucursal","asesor","fecha_ingreso","fecha_dispersion",
    "estatus","monto_propuesta","monto_final","segundo_estatus","observaciones",
    "score","telefono","correo","analista","fuente"
]

def cargar_clientes() -> pd.DataFrame:
    """
    Lee primero de Google Sheets (prioridad), luego de archivos locales
    """
    def _ensure_cols(df: pd.DataFrame) -> pd.DataFrame:
        df = df.copy().fillna("")
        for c in COLUMNS:
            if c not in df.columns:
                df[c] = ""
        return df[[c for c in COLUMNS if c in df.columns]]

    # 1) PRIMERO intentar Google Sheets (si está habilitado)
    if USE_GSHEETS:
        try:
            ws = _gs_open_worksheet(GSHEET_TAB)
            if ws is None:
                st.warning("No se pudo conectar a Google Sheets, usando datos locales")
                raise Exception("No connection")
                
            df = get_as_dataframe(ws, evaluate_formulas=True, dtype=str, header=0).dropna(how="all")
            if df is None or df.empty:
                df = pd.DataFrame(columns=COLUMNS)
            else:
                # Mensaje temporal: mostrar solo la primera vez por sesión
                try:
                    if not st.session_state.get('gs_load_msg_shown', False):
                        try:
                            st.toast(f"✅ Datos cargados desde Google Sheets: {len(df)} registros")
                        except Exception:
                            # Fallback seguro si st.toast no existe
                            st.success(f"✅ Datos cargados desde Google Sheets: {len(df)} registros")
                        st.session_state['gs_load_msg_shown'] = True
                except Exception:
                    # No romper si session_state no está disponible
                    try:
                        st.success(f"✅ Datos cargados desde Google Sheets: {len(df)} registros")
                    except Exception:
                        pass
                
                
            df = df.fillna("")
            for c in COLUMNS:
                if c not in df.columns:
                    df[c] = ""
            return df[COLUMNS].astype(str).fillna("")
        except Exception as e:
            st.warning(f"⚠️ No se pudo cargar desde Google Sheets: {str(e)}")

    # 2) Fallback a archivos locales
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

def guardar_clientes(df: pd.DataFrame):
    """
    Guarda la base en CSV y XLSX (respaldo). Evita NaNs y asegura columnas.
    """
    # Guardado local y opcional a Google Sheets (append/upsert)
    try:
        if df is None:
            return

        # asegurar columnas y tipo
        for c in COLUMNS:
            if c not in df.columns:
                df[c] = ""
        df_to_save = df[[c for c in COLUMNS if c in df.columns]].copy().fillna("").astype(str)

        # CSV (local)
        df_to_save.to_csv(CLIENTES_CSV, index=False, encoding="utf-8")

        # XLSX (respaldo)
        try:
            engine = None
            try:
                import xlsxwriter  # noqa
                engine = "xlsxwriter"
            except Exception:
                try:
                    import openpyxl  # noqa
                    engine = "openpyxl"
                except Exception:
                    engine = None

            if engine:
                with pd.ExcelWriter(CLIENTES_XLSX, engine=engine) as writer:
                    df_to_save.to_excel(writer, index=False, sheet_name="Clientes")
        except Exception:
            pass

        # --- Helpers para GSheet append/upsert ---
        def _ensure_columns(df: pd.DataFrame, cols: list[str]) -> pd.DataFrame:
            df = df.copy().fillna("")
            for c in cols:
                if c not in df.columns:
                    df[c] = ""
            return df[cols].astype(str).fillna("")

        def _sheet_to_df(ws) -> pd.DataFrame:
            dfsh = get_as_dataframe(ws, evaluate_formulas=True, dtype=str, header=0).dropna(how="all")
            if dfsh is None or dfsh.empty:
                return pd.DataFrame()
            return dfsh.fillna("").astype(str)

        def guardar_clientes_gsheet_append(df_nuevo: pd.DataFrame):
            """ Guarda clientes en modo append/upsert (sin sobrescribir todo) """
            if df_nuevo is None or df_nuevo.empty:
                return

            ws = _gs_open_worksheet(GSHEET_TAB)
            df_nuevo = _ensure_columns(df_nuevo, COLUMNS)

            # Asegurar que la primera fila de la hoja sea exactamente los encabezados esperados
            try:
                header_row = ws.row_values(1)
            except Exception:
                header_row = []
            # Normalizar strings de encabezado
            header_norm = [str(h).strip() for h in header_row]
            if header_norm[:len(COLUMNS)] != COLUMNS:
                try:
                    ws.update("A1", [COLUMNS])
                except Exception:
                    pass

            df_actual = _sheet_to_df(ws)
            if df_actual.empty:
                # Aseguramos encabezado y luego agregamos los datos
                try:
                    # actualizar encabezado (por si no existía)
                    ws.update("A1", [COLUMNS])
                except Exception:
                    pass
                rows = df_nuevo[COLUMNS].values.tolist()
                if rows:
                    try:
                        ws.append_rows(rows, value_input_option="RAW")
                    except Exception:
                        # último recurso: set_with_dataframe para escribir todo
                        try:
                            set_with_dataframe(ws, df_nuevo, include_index=False, include_column_header=True, resize=True)
                        except Exception:
                            pass
                return
                return

            df_actual = _ensure_columns(df_actual, COLUMNS)

            # Índices por ID
            idx_actual = {str(r["id"]): i for i, r in df_actual.reset_index(drop=True).iterrows() if str(r["id"]).strip() != ""}
            idx_nuevo  = {str(r["id"]): i for i, r in df_nuevo.reset_index(drop=True).iterrows() if str(r["id"]).strip() != ""}

            nuevos_ids = [i for i in idx_nuevo.keys() if i not in idx_actual]
            comunes_ids = [i for i in idx_nuevo.keys() if i in idx_actual]

            # 1) Agrega los nuevos
            if nuevos_ids:
                rows_to_append = df_nuevo.loc[df_nuevo["id"].astype(str).isin(nuevos_ids), COLUMNS].values.tolist()
                ws.append_rows(rows_to_append, value_input_option="RAW")

            # 2) Actualiza los existentes (si cambian)
            updates = []
            for _id in comunes_ids:
                row_new = df_nuevo.loc[idx_nuevo[_id], COLUMNS]
                row_old = df_actual.loc[idx_actual[_id], COLUMNS]
                if not row_new.equals(row_old):
                    fila = idx_actual[_id] + 2  # +2 por encabezado
                    # rango A.. según número columnas (obtener letra de columna correctamente)
                    col_a1 = gspread.utils.rowcol_to_a1(1, len(COLUMNS))  # e.g. 'P1'
                    # quitar los dígitos al final para obtener la letra(s) de columna
                    try:
                        import re
                        col_letter = re.sub(r"\d+$", "", col_a1)
                    except Exception:
                        col_letter = col_a1
                    rango = f"A{fila}:{col_letter}{fila}"
                    updates.append({
                        "range": rango,
                        "values": [row_new.tolist()]
                    })

            if updates:
                try:
                    ws.batch_update([{"range": u["range"], "values": u["values"]} for u in updates], value_input_option="RAW")
                except Exception as e:
                    try:
                        print(f"⚠️ Error en batch_update de clientes en GSheets: {e}")
                    except Exception:
                        pass

        HIST_COLUMNS_DEFAULT = ["fecha","accion","id","nombre","detalle","usuario"]

        def append_historial_gsheet(evento: dict):
            """ Agrega un registro al historial (una fila nueva) """
            ws = _gs_open_worksheet(GSHEET_HISTTAB)
            df_actual = _sheet_to_df(ws)
            if df_actual.empty:
                try:
                    ws.update(values=[HIST_COLUMNS_DEFAULT], range_name="A1")
                except Exception:
                    pass
            fila = [str(evento.get(col, "")) for col in HIST_COLUMNS_DEFAULT]
            try:
                ws.append_rows([fila], value_input_option="RAW")
            except Exception:
                pass

        # Enviar a Google Sheets si está activado
        if USE_GSHEETS:
            try:
                guardar_clientes_gsheet_append(df_to_save)
            except Exception as e:
                try:
                    print(f"⚠️ Error al guardar en Google Sheets: {e}")
                except Exception:
                    pass

    except Exception as e:
        try:
            st.error(f"Error guardando clientes: {e}")
        except Exception:
            pass

# Función para corregir IDs duplicados/vacíos
def _fix_missing_or_duplicate_ids(df: pd.DataFrame) -> pd.DataFrame:
    """Corrige IDs vacíos o duplicados en el DataFrame"""
    if df is None or df.empty:
        return df
    df = df.copy()
    if "id" not in df.columns:
        df["id"] = ""

    usados = set()
    def _nuevo_id_local(_df):
        base_id = 1000
        try:
            if not _df.empty and "id" in _df.columns:
                nums = []
                for x in _df["id"].astype(str):
                    if str(x).startswith("C"):
                        try:
                            nums.append(int(str(x).lstrip("C")))
                        except Exception:
                            continue
                if nums:
                    base_id = max(nums) + 1
                else:
                    base_id = base_id + len(_df) + 1
        except Exception:
            base_id = base_id + 1
        return f"C{base_id}"

    for i in df.index:
        cur = str(df.at[i, "id"]).strip()
        if not cur or cur in usados:
            # genera ID nuevo que no choque con usados ni con el df
            nuevo = _nuevo_id_local(df)
            while nuevo in usados or (df["id"] == nuevo).any():
                try:
                    num = int(nuevo[1:]) + 1
                except Exception:
                    num = 1000
                nuevo = f"C{num}"
            df.at[i, "id"] = nuevo
            usados.add(nuevo)
        else:
            usados.add(cur)
    return df

# Función para cargar y corregir datos de clientes
def cargar_y_corregir_clientes() -> pd.DataFrame:
    """Carga los clientes y corrige IDs duplicados/vacíos si es necesario"""
    df_cli = cargar_clientes()
    
    try:
        df_fixed = _fix_missing_or_duplicate_ids(df_cli)
        # solo guardar si hubo cambios (evitar escribir en disco/Sheets innecesariamente)
        try:
            changed = not df_fixed.equals(df_cli)
        except Exception:
            # en caso de error al comparar, guardar para mantener consistencia
            changed = True
        if changed:
            df_cli = df_fixed
            guardar_clientes(df_cli)
        else:
            df_cli = df_fixed
    except Exception:
        pass
    
    return df_cli# ---------- Historial y eliminación de clientes ----------
HISTORIAL_CSV = DATA_DIR / "historial.csv"

def cargar_historial() -> pd.DataFrame:
    """
    Lee el CSV de historial si existe; retorna DataFrame vacío con columnas esperadas si no.
    """
    # añadimos 'action' y 'actor' para saber quién hizo el cambio y qué tipo fue
    cols = ["id", "nombre", "estatus_old", "estatus_new", "segundo_old", "segundo_new", "observaciones", "action", "actor", "ts"]
    try:
        if HISTORIAL_CSV.exists():
            dfh = pd.read_csv(HISTORIAL_CSV, dtype=str).fillna("")
            for c in cols:
                if c not in dfh.columns:
                    dfh[c] = ""
            return dfh[cols].copy()
    except Exception:
        pass
    return pd.DataFrame(columns=cols)

def append_historial_gsheet(evento: dict):
    """
    Versión global para registrar historial en Google Sheets.
    Se crea si no existe encabezado y luego se hace append.
    Silenciosa ante cualquier excepción.
    """
    if not USE_GSHEETS:
        return
    try:
        ws = _gs_open_worksheet(GSHEET_HISTTAB)
        headers = ["fecha","accion","id","nombre","detalle","usuario"]
        try:
            existing_header = ws.row_values(1)
        except Exception:
            existing_header = []
        if not existing_header:
            try:
                ws.update("A1", [headers])
            except Exception:
                pass
        fila = [str(evento.get(col, "")) for col in headers]
        try:
            ws.append_rows([fila], value_input_option="RAW")
        except Exception:
            pass
    except Exception:
        pass

def append_historial(cid: str, nombre: str, estatus_old: str, estatus_new: str, seg_old: str, seg_new: str, observaciones: str = "", action: str = "ESTATUS MODIFICADO", actor: str | None = None):
    """
    Agrega una fila al historial de estatus (archivo CSV).
    action: 'crear'|'modificar'|'eliminar'|'importar' u otro texto libre.
    actor: nombre de usuario que realizó la acción; si no se pasa, se toma el usuario actual.
    """
    try:
        if actor is None:
            cu = current_user() or {}
            actor = cu.get("user") or cu.get("email") or "(sistema)"

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
        if HISTORIAL_CSV.exists():
            dfh = cargar_historial()
            dfh = pd.concat([dfh, pd.DataFrame([registro])], ignore_index=True)
        else:
            dfh = pd.DataFrame([registro])
        dfh.to_csv(HISTORIAL_CSV, index=False, encoding="utf-8")
        # También intentar escribir en Google Sheets (modo append) si está habilitado
        if USE_GSHEETS:
            try:
                evento = {
                    "fecha": registro.get("ts", ""),
                    "accion": registro.get("action", ""),
                    "id": registro.get("id", ""),
                    "nombre": registro.get("nombre", ""),
                    "detalle": registro.get("observaciones", ""),
                    "usuario": registro.get("actor", "")
                }
                try:
                    append_historial_gsheet(evento)
                except Exception:
                    pass
            except Exception:
                pass
    except Exception:
        # no bloquear la app por errores de historial
        pass

def eliminar_cliente(cid: str, df: pd.DataFrame, borrar_historial: bool = False) -> pd.DataFrame:
    """
    Elimina al cliente del DataFrame `df`, borra su carpeta de documentos y (opcionalmente) las entradas de historial.
    Retorna el DataFrame resultante (y guarda el CSV de clientes).
    """
    try:
        if cid is None or cid == "" or df is None or df.empty or "id" not in df.columns:
            return df
        # Borrar carpeta de documentos del cliente
        try:
            folder = DOCS_DIR / safe_name(str(cid))
            if folder.exists() and folder.is_dir():
                shutil.rmtree(folder)
        except Exception:
            pass

        # Eliminar de df
        df_new = df[df["id"] != cid].reset_index(drop=True)
        guardar_clientes(df_new)

        # --- NUEVO: eliminar también de la hoja de Google Sheets (si está habilitado) ---
        if USE_GSHEETS:
            try:
                ws = _gs_open_worksheet(GSHEET_TAB)
                vals = ws.get_all_values()
                if vals and len(vals) > 0:
                    header = [str(h).strip() for h in vals[0]]
                    # buscar índice de la columna 'id' (case/acentos tolerantemente)
                    id_col = None
                    for idx, h in enumerate(header):
                        if _norm_key(h) == _norm_key("id"):
                            id_col = idx
                            break
                    if id_col is not None:
                        rows_to_delete = []
                        # recorrer filas de datos (vals[1:] corresponde a filas físicas a partir de la 2)
                        for i in range(1, len(vals)):
                            try:
                                cell = vals[i][id_col] if id_col < len(vals[i]) else ""
                            except Exception:
                                cell = ""
                            if str(cell).strip() == str(cid):
                                # i -> índice en vals; la fila en la hoja es i+1 (1-based)
                                rows_to_delete.append(i + 1)
                        # borrar de abajo hacia arriba para no invalidar índices
                        for rownum in sorted(rows_to_delete, reverse=True):
                            try:
                                ws.delete_rows(rownum)
                            except Exception:
                                # fallback no crítico: intentar limpiar la fila en lugar de borrarla
                                try:
                                    # limpiar un rango amplio (A..Z) para evitar errores si delete_rows falla
                                    ws.update(f"A{rownum}:Z{rownum}", [[""] * 26])
                                except Exception:
                                    pass
            except Exception:
                # silenciar cualquier error de GSheets para no romper la app
                pass
        # -------------------------------------------------------

        # Borrar historial asociado si se solicita
        if borrar_historial:
            try:
                if HISTORIAL_CSV.exists():
                    dfh = cargar_historial()
                    dfh = dfh[dfh["id"] != cid].reset_index(drop=True)
                    dfh.to_csv(HISTORIAL_CSV, index=False, encoding="utf-8")
            except Exception:
                pass

        return df_new
    except Exception:
        return df

# --- AUTENTICACIÓN CON ROLES (admin / member) ---
import secrets
import base64

USERS_FILE = DATA_DIR / "users.json"   # { "users":[{"user": "...", "role":"admin|member", "salt":"...", "hash":"..."}] }
# Google Sheets tab name for users
GSHEET_USERSTAB = "users"

PERMISSIONS = {
    "admin":  {"manage_users": True,  "delete_client": True},
    "member": {"manage_users": False, "delete_client": False},
}

def do_rerun():
    """Forzar rerun compatible con varias versiones de Streamlit."""
    try:
        if hasattr(st, "experimental_rerun"):
            st.experimental_rerun()
            return
    except Exception:
        pass
    try:
        from streamlit.runtime.scriptrunner import RerunException  # type: ignore
        raise RerunException("Requested rerun")
    except Exception:
        pass
    try:
        from streamlit.script_runner import RerunException as _RerunOld  # type: ignore
        raise _RerunOld("Requested rerun (old)")
    except Exception:
        pass
    st.session_state["_need_rerun"] = not st.session_state.get("_need_rerun", False)
    try:
        st.stop()
    except Exception:
        return

def _hash_pw_pbkdf2(password: str, salt_hex: str | None = None) -> tuple[str, str]:
    if not salt_hex:
        salt_hex = secrets.token_hex(16)
    salt = bytes.fromhex(salt_hex)
    dk = hashlib.pbkdf2_hmac("sha256", (password or "").encode("utf-8"), salt, 100_000)
    return salt_hex, dk.hex()

def _verify_pw(password: str, salt_hex: str, hash_hex: str) -> bool:
    _, hh = _hash_pw_pbkdf2(password, salt_hex)
    return secrets.compare_digest(hh, (hash_hex or ""))

def cargar_usuarios_gsheet() -> dict:
    """
    Carga usuarios desde Google Sheets
    Retorna el mismo formato que load_users()
    """
    if not USE_GSHEETS:
        return {"users": []}
    
    try:
        ws = _gs_open_worksheet(GSHEET_USERSTAB)
        if ws is None:
            return {"users": []}
            
        df = get_as_dataframe(ws, evaluate_formulas=True, dtype=str, header=0).dropna(how="all")
        if df is None or df.empty:
            return {"users": []}
            
        users = []
        for _, row in df.iterrows():
            user_data = {
                "user": row.get("user", ""),
                "role": row.get("role", "member"),
                "salt": row.get("salt", ""),
                "hash": row.get("hash", "")
            }
            # Solo agregar usuarios válidos
            if user_data["user"] and user_data["salt"] and user_data["hash"]:
                users.append(user_data)
                
        return {"users": users}
        
    except Exception as e:
        st.error(f"Error cargando usuarios desde Google Sheets: {e}")
        return {"users": []}

def guardar_usuarios_gsheet(users_data: dict):
    """
    Guarda usuarios en Google Sheets
    """
    if not USE_GSHEETS:
        return
        
    try:
        ws = _gs_open_worksheet(GSHEET_USERSTAB)
        if ws is None:
            st.error("No se pudo abrir la pestaña de usuarios en Google Sheets")
            return
            
        # Preparar datos para guardar
        users_list = users_data.get("users", [])
        if not users_list:
            # Limpiar la hoja si no hay usuarios
            try:
                ws.clear()
            except Exception:
                pass
            return
            
        # Crear DataFrame
        df = pd.DataFrame(users_list)
        
        # Asegurar columnas en orden correcto
        column_order = ["user", "role", "salt", "hash"]
        for col in column_order:
            if col not in df.columns:
                df[col] = ""
                
        df = df[column_order]
        
        # Guardar en Google Sheets
        set_with_dataframe(ws, df, include_index=False, include_column_header=True, resize=True)
        
    except Exception as e:
        st.error(f"Error guardando usuarios en Google Sheets: {e}")

def load_users() -> dict:
    """
    Carga usuarios primero desde Google Sheets, luego desde archivo local como fallback
    """
    # 1) Intentar Google Sheets primero
    if USE_GSHEETS:
        gsheet_data = cargar_usuarios_gsheet()
        if gsheet_data and gsheet_data.get("users"):
            return gsheet_data
    
    # 2) Fallback a archivo local
    try:
        if USERS_FILE.exists():
            return json.loads(USERS_FILE.read_text(encoding="utf-8"))
    except Exception:
        pass
    
    return {"users": []}

def save_users(obj: dict):
    """
    Guarda usuarios en Google Sheets Y en archivo local (backup)
    """
    # 1) Guardar en Google Sheets (primario)
    if USE_GSHEETS:
        guardar_usuarios_gsheet(obj)
    
    # 2) Guardar en archivo local (backup)
    try:
        USERS_FILE.write_text(json.dumps(obj, indent=2, ensure_ascii=False), encoding="utf-8")
    except Exception as e:
        st.error(f"Error guardando usuarios localmente: {e}")

def sync_usuarios_local_to_gsheet():
    """
    Sincroniza usuarios desde el archivo local a Google Sheets
    Útil para migración inicial
    """
    try:
        local_data = load_users()
        guardar_usuarios_gsheet(local_data)
    except Exception as e:
        st.error(f"Error sincronizando usuarios: {e}")

def get_user(identifier: str) -> dict | None:
    """Buscar usuario por username o por email (compatibilidad backward).
    identifier: lo que ingresa el usuario (username); busca en 'user' o 'email'.
    """
    ident = (identifier or "").strip().lower()
    data = load_users()
    for u in data.get("users", []):
        if u.get("user", "").lower() == ident or u.get("email", "").lower() == ident:
            return u
    return None

def add_user(username: str, password: str, role: str = "member") -> tuple[bool, str]:
    uname = (username or "").strip()
    if not uname or not password:
        return False, "Usuario y contraseña son obligatorios."
    if role not in ("admin", "member"):
        return False, "Rol inválido."
    data = load_users()
    # comprueba duplicados en 'user' y en el antiguo 'email'
    lower_uname = uname.lower()
    if any((u.get("user","") or u.get("email","" )).lower() == lower_uname for u in data.get("users", [])):
        return False, "Ese usuario ya existe."
    salt_hex, hash_hex = _hash_pw_pbkdf2(password)
    data["users"].append({"user": uname, "role": role, "salt": salt_hex, "hash": hash_hex})
    save_users(data)
    return True, "Usuario creado."

def delete_user(username: str) -> tuple[bool, str]:
    name = (username or "").strip().lower()
    if not name:
        return False, "Usuario inválido."
    data = load_users()
    users = data.get("users", [])
    for i, u in enumerate(users):
        if (u.get("user","") or u.get("email","" )).lower() == name:
            users.pop(i)
            data["users"] = users
            save_users(data)
            return True, "Usuario eliminado."
    return False, "Usuario no encontrado."

def maybe_migrate_legacy_admin():
    legacy = DATA_DIR / "admin.json"
    if legacy.exists() and not USERS_FILE.exists():
        try:
            obj = json.loads(legacy.read_text(encoding="utf-8"))
            email = (obj.get("email","") or "").strip()
            if email:
                temp_pw = base64.urlsafe_b64encode(secrets.token_bytes(9)).decode("utf-8").rstrip("=")
                ok, _ = add_user(email, temp_pw, role="admin")
                if ok:
                    st.sidebar.info(f"Admin migrado: {email}. Contraseña temporal: {temp_pw}. Inicia y cámbiala.")
                    # Sincronizar con Google Sheets
                    if USE_GSHEETS:
                        try:
                            local_data = load_users()
                            guardar_usuarios_gsheet(local_data)
                        except Exception:
                            pass
                legacy.unlink(missing_ok=True)
        except Exception:
            pass

maybe_migrate_legacy_admin()

# session state for auth
if "auth_user" not in st.session_state:
    st.session_state["auth_user"] = None  # dict: {"email":..., "role":...}

def current_user():
    return st.session_state.get("auth_user")

def is_admin():
    u = current_user()
    return bool(u and u.get("role") == "admin")

def can(action: str) -> bool:
    u = current_user()
    role = (u or {}).get("role", "member")
    return PERMISSIONS.get(role, {}).get(action, False)

# Migración inicial de usuarios locales a Google Sheets si procede
def maybe_migrate_users_to_gsheet():
    """
    Migra usuarios del archivo local a Google Sheets si es la primera vez
    """
    if not USE_GSHEETS:
        return
        
    try:
        # Verificar si ya hay usuarios en Google Sheets
        gsheet_data = cargar_usuarios_gsheet()
        if not gsheet_data.get("users"):
            # No hay usuarios en GS, migrar desde local
            local_data = load_users()
            if local_data.get("users"):
                guardar_usuarios_gsheet(local_data)
                st.sidebar.success("✅ Usuarios migrados a Google Sheets")
    except Exception as e:
        st.sidebar.warning(f"⚠️ Error migrando usuarios: {e}")

# Setup inicial: si no hay usuarios, crear primer admin
maybe_migrate_users_to_gsheet()
users_data = load_users()
# Setup inicial: si no hay usuarios, crear primer admin
users_data = load_users()
if not users_data.get("users"):
    with st.sidebar.expander("Configurar administrador", expanded=True):
        st.warning("No hay usuarios. Crea el primer administrador.")
        _user = st.text_input("Usuario admin", key="setup_user")
        _pw1 = st.text_input("Contraseña", type="password", key="setup_pw1")
        _pw2 = st.text_input("Confirmar", type="password", key="setup_pw2")
        if st.button("Crear administrador"):
            if not _user or not _pw1:
                st.error("Usuario y contraseña obligatorios.")
            elif _pw1 != _pw2:
                st.error("Las contraseñas no coinciden.")
            else:
                ok, msg = add_user(_user, _pw1, role="admin")
                if ok:
                    st.success("Administrador creado. Inicia sesión.")
                    do_rerun()
                else:
                    st.error(msg)

# Login: renderizar en placeholder y eliminarlo al iniciar sesión
if not current_user():
    login_panel = st.sidebar.empty()
    with login_panel.form("login_form", clear_on_submit=True):
        st.markdown("### Iniciar sesión")
        luser = st.text_input("Usuario", key="login_user")
        lpw = st.text_input("Contraseña", type="password", key="login_pw")
        submitted = st.form_submit_button("Entrar")

    if submitted:
        u = get_user(luser)
        if u and _verify_pw(lpw, u.get("salt",""), u.get("hash","")):
            # establecer usuario y limpiar estado sensible
            st.session_state["auth_user"] = {"user": u.get("user") or u.get("email"), "role": u["role"]}
            for _k in ("login_pw", "login_user"):
                st.session_state.pop(_k, None)
            # quitar el formulario al instante; no forzar rerun inmediato (evita pantalla en blanco)
            login_panel.empty()
            st.toast(f"Bienvenido, {st.session_state['auth_user']['user']} ({u['role']}).", icon="✅")
        else:
            st.error("Credenciales inválidas.")

    # Si aún no hay usuario autenticado, detenemos la app aquí.
    if not current_user():
        st.stop()

# Sidebar: info + logout + admin panel
u = current_user()
st.sidebar.markdown(f"**Usuario:** {u.get('user') or u.get('email')} — _{u['role']}_")
if st.sidebar.button("Cerrar sesión"):
    st.session_state["auth_user"] = None
    # Limpiar filtros y campos de login/alta para evitar que queden visibles
    for k in ("f_suc","f_est","f_ases","ases_q","suc_q","est_q",
              "login_user","login_pw",
              "new_user_user","new_user_pw1","new_user_pw2",
              "setup_user","setup_pw1","setup_pw2"):
        st.session_state.pop(k, None)
    do_rerun()

if is_admin():
    # Agregar miembro del equipo: mostrar dentro de un expander para ahorrar espacio
    with st.sidebar.expander("Agregar miembro del equipo", expanded=False):
        with st.form("add_user_form", clear_on_submit=True):
            st.caption("Agregar miembro del equipo")
            nuser = st.text_input("Usuario del miembro", key="new_user_user")
            npw1 = st.text_input("Contraseña", type="password", key="new_user_pw1")
            npw2 = st.text_input("Confirmar contraseña", type="password", key="new_user_pw2")
            nrole = st.selectbox("Rol", ["member", "admin"], index=0, help="Por defecto: member", key="new_user_role")
            submitted = st.form_submit_button("Agregar usuario")

        if submitted:
            # Validaciones y feedback efímero
            if not nuser or not npw1:
                st.toast("Usuario y contraseña obligatorios.", icon="🚫")
            elif npw1 != npw2:
                st.toast("Las contraseñas no coinciden.", icon="🚫")
            else:
                ok, msg = add_user(nuser, npw1, role=nrole)
                st.toast(msg, icon="✅" if ok else "🚫")
                if ok:
                    # Forzar rerun para refrescar el sidebar y limpiar el form
                    do_rerun()

    # Mostrar lista de usuarios opcionalmente (toggle apagado por defecto)
    # -- Sincronización Usuarios (admin) --
    with st.sidebar.expander("🔄 Sincronización Usuarios", expanded=False):
        st.caption("Sincronizar usuarios entre Google Sheets y archivo local")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("📤 A Google Sheets", key="sync_to_gs"):
                local_data = load_users()
                guardar_usuarios_gsheet(local_data)
                st.success("Usuarios sincronizados a Google Sheets")
        
        with col2:
            if st.button("📥 Desde Google Sheets", key="sync_from_gs"):
                gsheet_data = cargar_usuarios_gsheet()
                if gsheet_data.get("users"):
                    USERS_FILE.write_text(
                        json.dumps(gsheet_data, indent=2, ensure_ascii=False), 
                        encoding="utf-8"
                    )
                    st.success("Usuarios sincronizados desde Google Sheets")
                    # Forzar rerun para recargar usuarios
                    do_rerun()

    show_users = st.sidebar.checkbox("Mostrar usuarios registrados", value=False, key="admin_show_users")
    if show_users:
        data = load_users()
        if data.get("users"):
            st.sidebar.caption("Usuarios registrados")
            st.sidebar.caption("Siempre dar doble click para confirmar.")
            # Mostrar tabla con botón eliminar por fila
            for x in data["users"]:
                uname = x.get("user") or x.get("email")
                role = x.get("role")
                col1, col2 = st.sidebar.columns([3,1])
                with col1:
                    st.write(f"{uname} — {role}")
                with col2:
                    # Evitar que el admin se borre a sí mismo
                    cur = current_user() or {}
                    cur_user = (cur.get("user") or cur.get("email"))
                    if uname != cur_user:
                        # flujo de confirmación en dos pasos para evitar borrados accidentales
                        confirm_key = f"confirm_del_{uname}"
                        confirm_input_key = f"confirm_del_input_{uname}"
                        if not st.session_state.get(confirm_key, False):
                            if st.sidebar.button("Eliminar", key=f"del_{uname}"):
                                # activar el modo de confirmación
                                st.session_state[confirm_key] = True
                                do_rerun()
                        else:
                            # Usar columnas del sidebar para mantener todo horizontal y evitar wrapping
                            c1, c2, c3 = st.sidebar.columns([3,1,1])
                            with c1:
                                # solo placeholder para ahorrar espacio visual
                                st.sidebar.text_input("", key=confirm_input_key, placeholder=uname)
                            with c2:
                                if st.sidebar.button("Eliminar", key=f"confirm_eliminar_{uname}"):
                                    st.toast("Escribe el usuario para confirmar.", icon="📝")
                                    typed = st.session_state.get(confirm_input_key, "").strip()
                                    if typed == str(uname):
                                        eliminar, msg = delete_user(uname)
                                        st.toast(msg, icon="✅" if eliminar else "🚫")
                                        # limpiar estado de confirmación
                                        st.session_state.pop(confirm_key, None)
                                        st.session_state.pop(confirm_input_key, None)
                                        if eliminar:
                                            do_rerun()
                                    else:
                                        st.toast("El texto no coincide. Escribe el nombre exacto para confirmar.", icon="🚫")
                            with c3:
                                if st.sidebar.button("Cancelar", key=f"confirm_cancel_{uname}"):
                                    st.session_state.pop(confirm_key, None)
                                    st.session_state.pop(confirm_input_key, None)
                                    do_rerun()
                    else:
                        st.write("")

    # -- Gestión de sucursales (solo admin) -- (ahora en expander para ahorrar espacio)
    st.sidebar.markdown("---")
    with st.sidebar.expander("Gestionar sucursales", expanded=False):
        st.caption("Agregar o eliminar sucursales")
        st.caption("Siempre dar doble click para confirmar.")

        # Mostrar lista editable de sucursales y añadir nueva
        suc_q = st.text_input("Nueva sucursal", key="admin_new_sucursal", placeholder="Ej. NUEVA_SUC")
        if st.button("➕ Agregar sucursal", key="admin_add_sucursal"):
            news = (st.session_state.get("admin_new_sucursal","") or "").strip()
            if not news:
                st.toast("Nombre vacío.", icon="🚫")
            else:
                # evitar duplicados (case-insensitive)
                if any(s.casefold() == news.casefold() for s in SUCURSALES):
                    st.toast("Esa sucursal ya existe.", icon="🚫")
                else:
                    SUCURSALES.append(news)
                    save_sucursales(SUCURSALES)
                    # usar toast global para feedback rápido
                    st.toast(f"Sucursal '{news}' agregada.", icon="✅")
                    # limpiar campo y forzar rerun para que el sidebar recargue
                    st.session_state.pop("admin_new_sucursal", None)
                    do_rerun()

        # Listado con opción de eliminar (confirmación)
        if SUCURSALES:
            st.caption("Sucursales registradas")
            for s in list(SUCURSALES):
                c1, c2 = st.columns([3,1])
                with c1:
                    st.write(s)
                with c2:
                    del_key = f"del_suc_{s}"
                    conf_key = f"del_suc_confirm_{s}"
                    if not st.session_state.get(conf_key, False):
                        if st.button("Eliminar", key=del_key):
                            # activar confirmación
                            st.session_state[conf_key] = True
                            do_rerun()
                    else:
                        # verificar que no haya clientes usando esa sucursal
                        in_use = False
                        try:
                            # cargar clientes y revisar columna 'sucursal'
                            _df_check = cargar_clientes()
                            if not _df_check.empty and 'sucursal' in _df_check.columns:
                                in_use = any(_norm_key(str(x)) == _norm_key(s) for x in _df_check['sucursal'].fillna(""))
                        except Exception:
                            in_use = False

                        if in_use:
                            st.write("En uso")
                            if st.button("Cancelar", key=f"cancel_del_suc_{s}"):
                                st.session_state.pop(conf_key, None)
                                do_rerun()
                        else:
                            # pedir confirmación final
                            colc1, colc2 = st.columns([2,1])
                            with colc1:
                                if st.button("Confirmar eliminar", key=f"confirm_del_suc_{s}"):
                                    try:
                                        SUCURSALES.remove(s)
                                        save_sucursales(SUCURSALES)
                                        st.toast(f"Sucursal '{s}' eliminada.", icon="✅")
                                    except Exception:
                                        # no bloquear si falla
                                        pass
                                    st.session_state.pop(conf_key, None)
                                    do_rerun()
                            with colc2:
                                if st.button("Cancelar", key=f"cancel_del_suc_{s}"):
                                    st.session_state.pop(conf_key, None)
                                    do_rerun()

# ---------- Sidebar (filtros + acciones) ----------
st.sidebar.title("👤 CRM")
st.sidebar.caption("Filtros")

# Botón para recargar datos desde Google Sheets
# IMPORTANTE: Usar este botón cuando los datos de Google Sheets no aparezcan en la app
if st.sidebar.button("🔄 Recargar datos", help="Fuerza la recarga de datos desde Google Sheets"):
    with st.spinner("Recargando datos desde Google Sheets..."):
        # Limpiar cache de session_state relacionado con carga
        for key in ['gs_load_msg_shown', 'gs_debug_shown']:
            st.session_state.pop(key, None)
        limpiar_cache_gsheets()
    st.toast("✅ Datos recargados desde Google Sheets", icon="✅")
    do_rerun()

# Cargar datos frescos para el sidebar
df_cli = cargar_y_corregir_clientes()

# Opciones base
SUC_LABEL_EMPTY = "(Sin sucursal)"
# CORREGIR: Manejar tanto valores vacíos ("") como None/NaN
sucursal_for_filter = df_cli["sucursal"].fillna("").replace({"": SUC_LABEL_EMPTY})
SUC_ALL  = sorted(set(SUCURSALES + [SUC_LABEL_EMPTY]))

# Recalcular campos derivados para filtros (asegurar que reflejen la versión en disco)
asesor_for_filter = df_cli["asesor"].fillna("").replace({"": "(Sin asesor)"})
# Normalizar variantes de la etiqueta "(Sin asesor)" (mayúsculas/minúsculas/espacios)
def _norm_sin_asesor_label(x: str) -> str:
    try:
        s = (x or "").strip()
    except Exception:
        s = ""
    if s.casefold() == "(sin asesor)":
        return "(Sin asesor)"
    return s

# Aplicar normalización y asegurar unicidad
ASES_ALL = sorted(list(dict.fromkeys([_norm_sin_asesor_label(x) for x in asesor_for_filter.unique().tolist()])))

EST_ALL = ESTATUS_OPCIONES.copy()

# --- NEW: Fuentes para filtro (se generan dinámicamente desde la base para que nuevas fuentes aparezcan automáticamente)
fuente_for_filter = df_cli["fuente"].fillna("").replace({"": "(Sin fuente)"})
FUENTE_ALL = sorted(list(dict.fromkeys([ (str(x).strip() if str(x).strip() else "(Sin fuente)") for x in fuente_for_filter.unique().tolist() ])))

# Controles “tipo selectbox” pero multi
f_suc  = selectbox_multi("Sucursales", SUC_ALL,  "f_suc")
f_ases = selectbox_multi("Asesores",   ASES_ALL, "f_ases")
f_est  = selectbox_multi("Estatus",    EST_ALL,  "f_est")
# NEW: añadir filtro de Fuente en el sidebar
f_fuente = selectbox_multi("Fuente", FUENTE_ALL, "f_fuente")

def _reset_filters():
    try:
        st.session_state["f_suc"] = SUC_ALL.copy()
        st.session_state["f_ases"] = ASES_ALL.copy()
        st.session_state["f_est"] = EST_ALL.copy()
        st.session_state["f_suc_all"] = True
        st.session_state["f_ases_all"] = True
        st.session_state["f_est_all"] = True
        st.session_state["f_suc_ms"] = SUC_ALL.copy()
        st.session_state["f_ases_ms"] = ASES_ALL.copy()
        st.session_state["f_est_ms"] = EST_ALL.copy()
        # NEW: reset para fuente
        st.session_state.setdefault("f_fuente", FUENTE_ALL.copy())
        st.session_state["f_fuente_all"] = True
        st.session_state["f_fuente_ms"] = FUENTE_ALL.copy()
        # token opcional para forzar lógica dependiente si la usas
        st.session_state["_filters_token"] = st.session_state.get("_filters_token", 0) + 1
    except Exception:
        pass

st.sidebar.button("🔁", key="btn_reset_filters", on_click=_reset_filters)

# Aplicar filtros: si no hay selección o está vacía, NO filtrar (mostrar todo)
try:
    # DEBUG: Mostrar estado de filtros en desarrollo
    # st.sidebar.write(f"DEBUG - f_suc: {len(f_suc) if f_suc else 0} de {len(SUC_ALL)}")
    # st.sidebar.write(f"DEBUG - f_ases: {len(f_ases) if f_ases else 0} de {len(ASES_ALL)}")
    # st.sidebar.write(f"DEBUG - f_est: {len(f_est) if f_est else 0} de {len(EST_ALL)}")
    
    # Sucursal: si está vacío o tiene todos, no filtrar
    if not f_suc or len(f_suc) == 0 or set(f_suc) == set(SUC_ALL):
        suc_mask = pd.Series(True, index=df_cli.index)
    else:
        suc_mask = sucursal_for_filter.isin(f_suc)

    # Asesor: si está vacío o tiene todos, no filtrar
    if not f_ases or len(f_ases) == 0 or set(f_ases) == set(ASES_ALL):
        asesor_mask = pd.Series(True, index=df_cli.index)
    else:
        asesor_mask = asesor_for_filter.isin(f_ases)

    # Estatus: si está vacío o tiene todos, no filtrar
    if not f_est or len(f_est) == 0 or set(f_est) == set(EST_ALL):
        est_mask = pd.Series(True, index=df_cli.index)
    else:
        est_mask = df_cli["estatus"].isin(f_est)

    # Fuente: si está vacío o tiene todos, no filtrar
    try:
        if not f_fuente or len(f_fuente) == 0 or set(f_fuente) == set(FUENTE_ALL):
            fuente_mask = pd.Series(True, index=df_cli.index)
        else:
            fuente_mask = fuente_for_filter.isin(f_fuente)
    except Exception:
        fuente_mask = pd.Series(True, index=df_cli.index)

except Exception as e:
    # Fallback seguro: no filtrar si algo falla
    st.sidebar.error(f"Error en filtros: {e}")
    suc_mask = pd.Series(True, index=df_cli.index)
    asesor_mask = pd.Series(True, index=df_cli.index)
    est_mask = pd.Series(True, index=df_cli.index)
    fuente_mask = pd.Series(True, index=df_cli.index)

df_ver = df_cli[suc_mask & est_mask & asesor_mask & fuente_mask].copy()

# Resumen
st.sidebar.markdown("---")
st.sidebar.subheader("📊 Resumen filtrado")
st.sidebar.metric("Clientes visibles", len(df_ver))
st.sidebar.metric("Total en base", len(df_cli))

# Añadir botón para descargar Excel del resumen filtrado (df_ver)
try:
    bio = io.BytesIO()
    engine = None
    try:
        import xlsxwriter  # type: ignore
        engine = "xlsxwriter"
    except Exception:
        try:
            import openpyxl  # type: ignore
            engine = "openpyxl"
        except Exception:
            engine = None

    if engine is None:
        st.sidebar.info("Instala 'openpyxl' o 'xlsxwriter' para habilitar descarga XLSX.")
    else:
        # Preparar DataFrame a exportar (ordenado por fechas si procede)
        try:
            df_export = sort_df_by_dates(df_ver) if (isinstance(df_ver, pd.DataFrame) and not df_ver.empty) else df_ver.copy()
        except Exception:
            df_export = df_ver.copy() if isinstance(df_ver, pd.DataFrame) else pd.DataFrame()

        with pd.ExcelWriter(bio, engine=engine) as writer:
            try:
                df_export.to_excel(writer, index=False, sheet_name="Filtrados")
            except Exception:
                # fallback: intentar convertir todo a strings y volver a escribir
                try:
                    df_export.astype(str).to_excel(writer, index=False, sheet_name="Filtrados")
                except Exception:
                    pass
        bio.seek(0)
        if st.sidebar.download_button(
            "⬇️ Descargar Excel (filtrados)",
            data=bio.getvalue(),
            file_name="clientes_filtrados.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            key="dl_filtrados_sidebar"
        ):
            try:
                actor = (current_user() or {}).get("user") or (current_user() or {}).get("email")
                append_historial(
                "", "", "", "", "", "",
                "Descarga de Excel filtrados",
                action="DESCARGA ZIP",  # o "DOCUMENTOS", según quieras categorizarlo
                actor=actor
                )
            except Exception:
                    pass
except Exception:
    # no bloquear la UI si algo falla
    pass

# ---------- Main UI con pestañas ----------  # NEW
# Header profesional
render_professional_header()

tab_dash, tab_cli, tab_docs, tab_import, tab_hist, tab_asesores = st.tabs(
    ["📊 Dashboard", "📋 Clientes", "📎 Documentos", "📥 Importar", "🗂️ Historial", " 👥 Asesores"]
)

# ===== Dashboard =====
with tab_dash:
    # Cargar datos frescos para el dashboard
    df_cli = cargar_y_corregir_clientes()
    
    if df_cli.empty:
        st.info("Sin clientes aún.")
    else:
        # 🎯 KPIs PRINCIPALES EN LA PARTE SUPERIOR
        st.subheader("📊 KPIs Principales")
        
        # Preparar datos para KPIs
        total_clientes = len(df_cli)
        estatus_counts = df_cli["estatus"].fillna("").value_counts()
        
        # Calcular KPIs principales
        dispersados = estatus_counts.get("DISPERSADO", 0)
        en_proceso = sum([
            estatus_counts.get("EN ONBOARDING", 0),
            estatus_counts.get("PENDIENTE CLIENTE", 0),
            estatus_counts.get("PROPUESTA", 0),
            estatus_counts.get("PENDIENTE DOC", 0)
        ])
        rechazados = sum([
            estatus_counts.get("REC SOBREENDEUDAMIENTO", 0),
            estatus_counts.get("REC NO CUMPLE POLITICAS", 0),
            estatus_counts.get("REC EDAD", 0)
        ])
        
        # Mostrar KPIs profesionales en columnas
        kpi1, kpi2, kpi3, kpi4 = st.columns(4)
        
        with kpi1:
            st.metric(
                label="👥 Total de Clientes",
                value=total_clientes,
                help="Número total de clientes en la base de datos"
            )
        
        with kpi2:
            tasa_exito = (dispersados / total_clientes * 100) if total_clientes > 0 else 0
            st.metric(
                label="✅ Dispersados (Éxito)",
                value=dispersados,
                delta=f"{tasa_exito:.1f}% del total",
                help="Clientes que han completado exitosamente el proceso"
            )
        
        with kpi3:
            tasa_proceso = (en_proceso / total_clientes * 100) if total_clientes > 0 else 0
            st.metric(
                label="⏳ En Proceso",
                value=en_proceso,
                delta=f"{tasa_proceso:.1f}% del total",
                help="Clientes en onboarding, pendientes o en evaluación"
            )
        
        with kpi4:
            tasa_rechazo = (rechazados / total_clientes * 100) if total_clientes > 0 else 0
            st.metric(
                label="❌ Rechazados",
                value=rechazados,
                delta=f"{tasa_rechazo:.1f}% del total",
                help="Clientes rechazados por diversos motivos"
            )
        
        st.markdown("---")
        
        # 🔄 TABS SECUNDARIAS PARA ANÁLISIS DETALLADO
        dash_tab1, dash_tab2, dash_tab3 = st.tabs([
            "📊 Por Estatus", 
            "📅 Por Fecha", 
            "🏢 Por Sucursal/Asesor"
        ])
        
        # 📊 TAB 1: POR ESTATUS
        with dash_tab1:
            st.subheader("Análisis por Estatus")
            
            # Solo mostrar estatus con valores > 0 (más limpio)
            estatus_data = df_cli["estatus"].fillna("(Sin estatus)").value_counts()
            estatus_data = estatus_data[estatus_data > 0]  # Filtrar solo valores > 0
            
            if estatus_data.empty:
                st.info("No hay datos de estatus para mostrar.")
            else:
                # Convertir a DataFrame y agregar porcentajes
                estatus_df = estatus_data.reset_index()
                estatus_df.columns = ["estatus", "cantidad"]
                estatus_df["porcentaje"] = (estatus_df["cantidad"] / total_clientes * 100).round(1)
                
                # Ordenar por cantidad (descendente)
                estatus_df = estatus_df.sort_values("cantidad", ascending=False)
                
                col1, col2 = st.columns([1, 2])
                
                with col1:
                    # Métricas con porcentajes del total
                    st.markdown("**Distribución detallada:**")
                    for _, row in estatus_df.iterrows():
                        st.metric(
                            label=row["estatus"],
                            value=f"{int(row['cantidad'])} ({row['porcentaje']}%)"
                        )
                
                with col2:
                    # Gráfico horizontal (más fácil de leer)
                    chart = alt.Chart(estatus_df).mark_bar(
                        cornerRadiusTopRight=4,
                        cornerRadiusBottomRight=4
                    ).encode(
                        x=alt.X("cantidad:Q", 
                               axis=alt.Axis(title="Cantidad de Clientes"),
                               scale=alt.Scale(domain=[0, estatus_df["cantidad"].max() * 1.1])),
                        y=alt.Y("estatus:N", 
                               sort="-x", 
                               axis=alt.Axis(title="Estatus")),
                        color=alt.Color("estatus:N", 
                                       scale=alt.Scale(scheme="category20"),
                                       legend=None),
                        tooltip=[
                            alt.Tooltip("estatus:N", title="Estatus"),
                            alt.Tooltip("cantidad:Q", title="Cantidad"),
                            alt.Tooltip("porcentaje:Q", title="Porcentaje (%)", format=".1f")
                        ]
                    ).properties(
                        height=max(300, len(estatus_df) * 40),
                        title="Distribución de Clientes por Estatus"
                    )
                    
                    # Agregar etiquetas con valores
                    text = alt.Chart(estatus_df).mark_text(
                        align="left",
                        baseline="middle",
                        dx=5,
                        fontSize=11,
                        fontWeight="bold"
                    ).encode(
                        x=alt.X("cantidad:Q"),
                        y=alt.Y("estatus:N", sort="-x"),
                        text=alt.Text("cantidad:Q", format="d"),
                        color=alt.value("black")
                    )
                    
                    st.altair_chart(chart + text, use_container_width=True)
        
        # 📅 TAB 2: POR FECHA
        with dash_tab2:
            st.subheader("Análisis Temporal")
            
            # Selector de período predefinido
            periodo_options = {
                "Último mes": 30,
                "Últimos 3 meses": 90,
                "Últimos 6 meses": 180,
                "Último año": 365,
                "Todo el histórico": None,
                "Personalizado": "custom"
            }
            
            col_periodo, col_custom = st.columns([1, 2])
            
            with col_periodo:
                periodo_seleccionado = st.selectbox(
                    "Seleccionar período:",
                    list(periodo_options.keys()),
                    index=0
                )
            
            # Determinar fechas según selección
            date_col = None
            for c in ("fecha_ingreso", "fecha_dispersion"):
                if c in df_cli.columns:
                    date_col = c
                    break
            
            if date_col is None:
                st.warning("No se encontraron columnas de fecha válidas.")
            else:
                df_temp = df_cli.copy()
                df_temp[date_col] = pd.to_datetime(df_temp[date_col], errors="coerce")
                df_temp = df_temp.dropna(subset=[date_col])
                
                if df_temp.empty:
                    st.warning("No hay datos con fechas válidas.")
                else:
                    today = pd.Timestamp.now()
                    
                    if periodo_seleccionado == "Personalizado":
                        with col_custom:
                            fecha_min = df_temp[date_col].min().date()
                            fecha_max = df_temp[date_col].max().date()
                            
                            rango_fechas = st.date_input(
                                "Seleccionar rango:",
                                value=(fecha_min, fecha_max),
                                min_value=fecha_min,
                                max_value=fecha_max
                            )
                            
                            if isinstance(rango_fechas, tuple) and len(rango_fechas) == 2:
                                fecha_inicio, fecha_fin = rango_fechas
                            else:
                                fecha_inicio = fecha_fin = rango_fechas
                    else:
                        dias = periodo_options[periodo_seleccionado]
                        if dias is None:  # Todo el histórico
                            fecha_inicio = df_temp[date_col].min().date()
                            fecha_fin = df_temp[date_col].max().date()
                        else:
                            fecha_fin = today.date()
                            fecha_inicio = (today - pd.Timedelta(days=dias)).date()
                    
                    # Filtrar datos por período
                    mask = (df_temp[date_col].dt.date >= fecha_inicio) & (df_temp[date_col].dt.date <= fecha_fin)
                    df_periodo = df_temp[mask].copy()
                    
                    if df_periodo.empty:
                        st.info("No hay datos en el período seleccionado.")
                    else:
                        # KPIs del período
                        st.markdown("**KPIs del período seleccionado:**")
                        
                        total_periodo = len(df_periodo)
                        dispersados_periodo = len(df_periodo[df_periodo["estatus"] == "DISPERSADO"])
                        tasa_conversion = (dispersados_periodo / total_periodo * 100) if total_periodo > 0 else 0
                        
                        kpi_col1, kpi_col2, kpi_col3 = st.columns(3)
                        
                        with kpi_col1:
                            st.metric("Total en período", total_periodo)
                        with kpi_col2:
                            st.metric("Dispersados", dispersados_periodo)
                        with kpi_col3:
                            st.metric("Tasa de conversión", f"{tasa_conversion:.1f}%")
                        
                        st.markdown("---")
                        
                        # Gráfico de evolución temporal (por mes)
                        st.markdown("**Evolución mensual:**")
                        
                        df_mensual = df_periodo.copy()
                        df_mensual["año_mes"] = df_mensual[date_col].dt.to_period("M")
                        evolucion = df_mensual.groupby("año_mes").size().reset_index(name="cantidad")
                        evolucion["fecha"] = evolucion["año_mes"].astype(str)
                        
                        if len(evolucion) > 0:
                            line_chart = alt.Chart(evolucion).mark_line(
                                point=True,
                                strokeWidth=3
                            ).encode(
                                x=alt.X("fecha:O", axis=alt.Axis(title="Mes", labelAngle=-45)),
                                y=alt.Y("cantidad:Q", axis=alt.Axis(title="Número de Clientes")),
                                tooltip=["fecha:O", "cantidad:Q"]
                            ).properties(
                                height=300,
                                title="Evolución de Clientes por Mes"
                            )
                            
                            st.altair_chart(line_chart, use_container_width=True)
                        
                        # Gráfico de dona: Distribución por estatus en el período
                        st.markdown("**Distribución por estatus en el período:**")
                        
                        estatus_periodo = df_periodo["estatus"].fillna("(Sin estatus)").value_counts()
                        estatus_periodo_df = estatus_periodo.reset_index()
                        estatus_periodo_df.columns = ["estatus", "cantidad"]
                        # Agregar porcentaje como columna calculada
                        estatus_periodo_df["porcentaje"] = (estatus_periodo_df["cantidad"] / total_periodo * 100).round(1)
                        
                        dona_chart = alt.Chart(estatus_periodo_df).mark_arc(
                            innerRadius=50,
                            outerRadius=120
                        ).encode(
                            theta=alt.Theta("cantidad:Q"),
                            color=alt.Color("estatus:N", scale=alt.Scale(scheme="category20")),
                            tooltip=[
                                alt.Tooltip("estatus:N", title="Estatus"),
                                alt.Tooltip("cantidad:Q", title="Cantidad"),
                                alt.Tooltip("porcentaje:Q", title="Porcentaje (%)", format=".1f")
                            ]
                        ).properties(
                            height=300,
                            title="Distribución por Estatus"
                        )
                        
                        st.altair_chart(dona_chart, use_container_width=True)
        
        # 🏢 TAB 3: POR SUCURSAL/ASESOR
        with dash_tab3:
            st.subheader("Análisis por Organización")
            
            # Sub-tabs: Sucursales, Asesores, Fuentes
            sub_tab1, sub_tab2, sub_tab3 = st.tabs(["🏢 Sucursales", "👥 Asesores", "📢 Fuentes"])
            
            # SUB-TAB: SUCURSALES
            with sub_tab1:
                sucursal_counts = df_cli["sucursal"].fillna("(Sin sucursal)").value_counts()
                sucursal_counts = sucursal_counts[sucursal_counts > 0]
                
                if sucursal_counts.empty:
                    st.info("No hay datos de sucursales para mostrar.")
                else:
                    sucursal_df = sucursal_counts.reset_index()
                    sucursal_df.columns = ["sucursal", "cantidad"]
                    sucursal_df["porcentaje"] = (sucursal_df["cantidad"] / total_clientes * 100).round(1)
                    
                    col1, col2 = st.columns([1, 2])
                    
                    with col1:
                        st.markdown("**Distribución por sucursal:**")
                        st.dataframe(
                            sucursal_df.assign(
                                **{"Porcentaje": sucursal_df["porcentaje"].astype(str) + "%"}
                            )[["sucursal", "cantidad", "Porcentaje"]],
                            use_container_width=True,
                            hide_index=True
                        )
                    
                    with col2:
                        chart_suc = alt.Chart(sucursal_df).mark_arc(
                            innerRadius=30,
                            outerRadius=100
                        ).encode(
                            theta=alt.Theta("cantidad:Q"),
                            color=alt.Color("sucursal:N", scale=alt.Scale(scheme="set3")),
                            tooltip=[
                                alt.Tooltip("sucursal:N", title="Sucursal"),
                                alt.Tooltip("cantidad:Q", title="Cantidad"),
                                alt.Tooltip("porcentaje:Q", title="Porcentaje (%)", format=".1f")
                            ]
                        ).properties(
                            height=300,
                            title="Distribución por Sucursal"
                        )
                        
                        st.altair_chart(chart_suc, use_container_width=True)
            
            # SUB-TAB: ASESORES
            with sub_tab2:
                # Para la sección de asesores del dashboard, usar datos filtrados EXCEPTO por asesor
                # para mostrar todos los asesores (misma lógica que en tab_asesores)
                try:
                    # Aplicar filtros SIN incluir el filtro de asesor
                    sucursal_for_filter = df_cli["sucursal"].fillna("").replace({"": "(Sin sucursal)"})
                    fuente_for_filter = df_cli["fuente"].fillna("").replace({"": "(Sin fuente)"})
                    
                    # Aplicar solo filtros de sucursal, estatus y fuente (NO asesor)
                    if not f_suc or len(f_suc) == 0 or set(f_suc) == set(SUC_ALL):
                        suc_mask_dash = pd.Series(True, index=df_cli.index)
                    else:
                        suc_mask_dash = sucursal_for_filter.isin(f_suc)

                    if not f_est or len(f_est) == 0 or set(f_est) == set(EST_ALL):
                        est_mask_dash = pd.Series(True, index=df_cli.index)
                    else:
                        est_mask_dash = df_cli["estatus"].isin(f_est)

                    if not f_fuente or len(f_fuente) == 0 or set(f_fuente) == set(FUENTE_ALL):
                        fuente_mask_dash = pd.Series(True, index=df_cli.index)
                    else:
                        fuente_mask_dash = fuente_for_filter.isin(f_fuente)
                    
                    # Datos filtrados para asesores (sin filtro de asesor)
                    df_asesor_dash = df_cli[suc_mask_dash & est_mask_dash & fuente_mask_dash]
                except Exception:
                    # Fallback: usar todos los datos
                    df_asesor_dash = df_cli
                
                asesor_counts = df_asesor_dash["asesor"].fillna("(Sin asesor)").value_counts()
                asesor_counts = asesor_counts[asesor_counts > 0]
                
                if asesor_counts.empty:
                    st.info("No hay datos de asesores para mostrar.")
                else:
                    # Top 10 asesores + "Otros" (cuando hay muchos)
                    if len(asesor_counts) > 10:
                        top_10 = asesor_counts.head(10)
                        otros = asesor_counts.tail(len(asesor_counts) - 10).sum()
                        
                        # Crear serie combinada
                        asesor_final = pd.concat([top_10, pd.Series([otros], index=["Otros"])])
                    else:
                        asesor_final = asesor_counts
                    
                    asesor_df = asesor_final.reset_index()
                    asesor_df.columns = ["asesor", "cantidad"]
                    # Usar el total de clientes filtrados para calcular porcentajes
                    total_filtrados = len(df_asesor_dash)
                    asesor_df["porcentaje"] = (asesor_df["cantidad"] / total_filtrados * 100).round(1) if total_filtrados > 0 else 0
                    
                    col1, col2 = st.columns([1, 2])
                    
                    with col1:
                        st.markdown("**Top asesores:**")
                        st.dataframe(
                            asesor_df.assign(
                                **{"Porcentaje": asesor_df["porcentaje"].astype(str) + "%"}
                            )[["asesor", "cantidad", "Porcentaje"]],
                            use_container_width=True,
                            hide_index=True
                        )
                    
                    with col2:
                        # Gráfico horizontal para asesores (mejor legibilidad)
                        chart_ases = alt.Chart(asesor_df).mark_bar(
                            cornerRadiusTopRight=4,
                            cornerRadiusBottomRight=4
                        ).encode(
                            x=alt.X("cantidad:Q", axis=alt.Axis(title="Cantidad")),
                            y=alt.Y("asesor:N", sort="-x", axis=alt.Axis(title="Asesor")),
                            color=alt.Color("asesor:N", scale=alt.Scale(scheme="category20"), legend=None),
                            tooltip=[
                                alt.Tooltip("asesor:N", title="Asesor"),
                                alt.Tooltip("cantidad:Q", title="Cantidad"),
                                alt.Tooltip("porcentaje:Q", title="Porcentaje (%)", format=".1f")
                            ]
                        ).properties(
                            height=max(300, len(asesor_df) * 30),
                            title="Distribución por Asesor"
                        )
                        
                        st.altair_chart(chart_ases, use_container_width=True)
            
            # SUB-TAB: FUENTES
            with sub_tab3:
                fuente_counts = df_cli["fuente"].fillna("(Sin fuente)").value_counts()
                fuente_counts = fuente_counts[fuente_counts > 0]
                
                if fuente_counts.empty:
                    st.info("No hay datos de fuentes para mostrar.")
                else:
                    fuente_df = fuente_counts.reset_index()
                    fuente_df.columns = ["fuente", "cantidad"]
                    fuente_df["porcentaje"] = (fuente_df["cantidad"] / total_clientes * 100).round(1)
                    
                    col1, col2 = st.columns([1, 2])
                    
                    with col1:
                        st.markdown("**Distribución por fuente:**")
                        st.dataframe(
                            fuente_df.assign(
                                **{"Porcentaje": fuente_df["porcentaje"].astype(str) + "%"}
                            )[["fuente", "cantidad", "Porcentaje"]],
                            use_container_width=True,
                            hide_index=True
                        )
                    
                    with col2:
                        # Gráfico de dona para fuentes
                        chart_fuente = alt.Chart(fuente_df).mark_arc(
                            innerRadius=40,
                            outerRadius=110
                        ).encode(
                            theta=alt.Theta("cantidad:Q"),
                            color=alt.Color("fuente:N", scale=alt.Scale(scheme="pastel1")),
                            tooltip=[
                                alt.Tooltip("fuente:N", title="Fuente"),
                                alt.Tooltip("cantidad:Q", title="Cantidad"),
                                alt.Tooltip("porcentaje:Q", title="Porcentaje (%)", format=".1f")
                            ]
                        ).properties(
                            height=300,
                            title="Distribución por Fuente de Captación"
                        )
                        
                        st.altair_chart(chart_fuente, use_container_width=True)

# ===== Clientes (alta + edición) =====
with tab_cli:
    # Cargar datos frescos para la pestaña de clientes
    df_cli = cargar_y_corregir_clientes()
    
    st.subheader("➕ Agregar cliente")
    with st.expander("Formulario de alta", expanded=False):  # UI más limpia

        # --- NEW: eliminar el selectbox "Asesor" (se pide quitar el "botoncito").
        # Mantener sólo el checkbox para crear un nuevo asesor y el input para su nombre.
        st.checkbox("Nuevo asesor (marca para escribir nombre y apellido)", key="form_new_asesor_toggle", help="Marca para ingresar manualmente el nombre y apellido del asesor")
        if st.session_state.get("form_new_asesor_toggle", False):
            st.text_input("Nombre y apellido del nuevo asesor", placeholder="Ej. Juan Pérez", key="form_nuevo_asesor")
        # --- END NEW ---

        with st.form("form_alta_cliente", clear_on_submit=True):
            c1, c2, c3 = st.columns(3)
            with c1:
                id_n = st.text_input("ID (opcional)", key="form_id")
                nombre_n = st.text_input("Nombre *")
                sucursal_n = st.selectbox("Sucursal *", SUCURSALES)

                # REPLACED: permitir elegir un asesor existente dentro del form,
                # o usar el "Nuevo asesor" si el checkbox (fuera del form) está marcado.
                raw_ases = [a for a in df_cli["asesor"].fillna("").unique() if str(a).strip()]
                asesores_exist = sorted(list(dict.fromkeys([_norm_sin_asesor_label(a) for a in raw_ases])))
                # Construir opciones sin duplicados (asegurando la etiqueta estándar "(Sin asesor)")
                asesores_choices = list(dict.fromkeys(["(Sin asesor)"] + asesores_exist))
                asesor_select = st.selectbox("Asesor", asesores_choices, key="form_ases_select")

                if st.session_state.get("form_new_asesor_toggle", False):
                    # si el usuario marcó "Nuevo asesor" usamos el texto ingresado (tiene prioridad)
                    asesor_n = st.session_state.get("form_nuevo_asesor", "").strip()
                else:
                    # usar la selección del selectbox (o '' si eligió "(Sin asesor)")
                    asesor_n = "" if asesor_select == "(Sin asesor)" else asesor_select

                analista_n = st.text_input("Analista")
            with c2:
                fecha_ingreso_n = st.date_input("Fecha ingreso", value=date.today())
                fecha_dispersion_n = st.date_input("Fecha dispersión", value=date.today())
                estatus_n = st.selectbox("Estatus", ESTATUS_OPCIONES, index=0)
                segundo_estatus_n = st.selectbox("Segundo estatus", SEGUNDO_ESTATUS_OPCIONES, index=0)
            with c3:
                monto_prop_n = st.text_input("Monto propuesta", value="")
                monto_final_n = st.text_input("Monto final", value="")
                score_n = st.text_input("Score", value="")
                telefono_n = st.text_input("Teléfono")
                correo_n = st.text_input("Correo")
                fuente_n = st.text_input("Fuente", value="")
            obs_n = st.text_area("Observaciones")

            st.markdown("**Documentos:**")
            up_estado = st.file_uploader("Estado de cuenta", type=DOC_CATEGORIAS["estado_cuenta"], accept_multiple_files=True, key="doc_estado")
            up_buro   = st.file_uploader("Buró de crédito", type=DOC_CATEGORIAS["buro_credito"], accept_multiple_files=True, key="doc_buro")
            up_solic  = st.file_uploader("Solicitud", type=DOC_CATEGORIAS["solicitud"], accept_multiple_files=True, key="doc_solic")
            up_otros = st.file_uploader("Otros", type=None, accept_multiple_files=True, key="doc_otros")
            st.markdown("Dar doble click para confirmar.")
            if st.form_submit_button("Guardar cliente"):
                
                if not nombre_n.strip():
                    st.warning("El nombre es obligatorio.")
                else:
                    # validar nuevo asesor si corresponde
                    if st.session_state.get("form_new_asesor_toggle", False) and not st.session_state.get("form_nuevo_asesor", "").strip():
                        st.warning("Cuando seleccionas 'Nuevo asesor' debes ingresar el nombre y apellido del asesor.")
                    else:
                        # usar ID proporcionado si existe y es único; si no, generar uno nuevo
                        provided = (id_n or "").strip()
                        if provided:
                            # sanitizar y validar unicidad
                            cid_candidate = safe_name(provided)
                            if cid_candidate in df_cli["id"].astype(str).tolist():
                                st.warning(f"El ID '{cid_candidate}' ya existe. Elige otro o deja vacío para generar uno.")
                                # no continuar con la creación
                                st.stop()
                            cid = cid_candidate
                        else:
                            cid = nuevo_id_cliente(df_cli)
                        # usar asesor_n calculado arriba (puede ser '')
                        asesor_final = find_matching_asesor(asesor_n.strip(), df_cli)
                        nuevo = {
                            "id": cid,
                            "nombre": nombre_n.strip(),
                            "sucursal": sucursal_n,
                            "asesor": asesor_final,
                            "fecha_ingreso": str(fecha_ingreso_n),
                            "fecha_dispersion": str(fecha_dispersion_n),
                            "estatus": estatus_n,
                            "monto_propuesta": str(monto_prop_n).strip(),
                            "monto_final": str(monto_final_n).strip(),
                            "segundo_estatus": segundo_estatus_n,
                            "observaciones": obs_n.strip(),
                            "score": str(score_n).strip(),
                            "telefono": telefono_n.strip(),
                            "correo": correo_n.strip(),
                            "analista": analista_n.strip(),
                            "fuente": fuente_n.strip(),
                        }
                        base = pd.concat([df_cli, pd.DataFrame([nuevo])], ignore_index=True)
                        guardar_clientes(base)
                        # registrar creación en historial
                        actor = (current_user() or {}).get("user") or (current_user() or {}).get("email")
                        append_historial(cid, nuevo.get("nombre", ""), "", nuevo.get("estatus", ""), "", nuevo.get("segundo_estatus", ""), f"Creado por {actor}", action="CLIENTE AGREGADO", actor=actor)

                        # Guardar documentos (auto refresh al terminar) — acumular y registrar 1 sola entrada en historial
                        subidos_lote = []
                        if up_estado:   subidos_lote += subir_docs(cid, up_estado,   prefijo="estado_")
                        if up_buro:     subidos_lote += subir_docs(cid, up_buro,     prefijo="buro_")
                        if up_solic:    subidos_lote += subir_docs(cid, up_solic,    prefijo="solic_")
                        #if up_contrato: subidos_lote += subir_docs(cid, up_contrato, prefijo="contrato_")
                        if up_otros:    subidos_lote += subir_docs(cid, up_otros,    prefijo="otros_")

                        if subidos_lote:
                            actor = (current_user() or {}).get("user") or (current_user() or {}).get("email")
                            append_historial(
                                cid, nuevo.get("nombre",""),
                                nuevo.get("estatus",""), nuevo.get("estatus",""),
                                nuevo.get("segundo_estatus",""), nuevo.get("segundo_estatus",""),
                                f"Subidos: {', '.join(subidos_lote)}",
                                action="DOCUMENTOS", actor=actor
                            )

                        st.success(f"Cliente {cid} creado ✅")
                        do_rerun()  # NEW: refresca todo

    st.subheader("📋 Lista de clientes")
    
    # APLICAR MISMA CORRECCIÓN: Para la pestaña de clientes, usar datos filtrados EXCEPTO por asesor
    # para mostrar todos los clientes (misma lógica que en tab_asesores)
    try:
        # Aplicar filtros SIN incluir el filtro de asesor
        sucursal_for_filter_cli = df_cli["sucursal"].fillna("").replace({"": "(Sin sucursal)"})
        fuente_for_filter_cli = df_cli["fuente"].fillna("").replace({"": "(Sin fuente)"})
        
        # Aplicar solo filtros de sucursal, estatus y fuente (NO asesor)
        if not f_suc or len(f_suc) == 0 or set(f_suc) == set(SUC_ALL):
            suc_mask_cli = pd.Series(True, index=df_cli.index)
        else:
            suc_mask_cli = sucursal_for_filter_cli.isin(f_suc)

        if not f_est or len(f_est) == 0 or set(f_est) == set(EST_ALL):
            est_mask_cli = pd.Series(True, index=df_cli.index)
        else:
            est_mask_cli = df_cli["estatus"].isin(f_est)

        if not f_fuente or len(f_fuente) == 0 or set(f_fuente) == set(FUENTE_ALL):
            fuente_mask_cli = pd.Series(True, index=df_cli.index)
        else:
            fuente_mask_cli = fuente_for_filter_cli.isin(f_fuente)
        
        # Datos filtrados para clientes (sin filtro de asesor)
        df_clientes_mostrar = df_cli[suc_mask_cli & est_mask_cli & fuente_mask_cli].copy()
    except Exception:
        # Fallback: usar df_ver si hay error
        df_clientes_mostrar = df_ver.copy()
    
    if df_clientes_mostrar.empty:
        st.info("No hay clientes con los filtros seleccionados.")
    else:
        colcfg = {
            "id": st.column_config.TextColumn("ID", disabled=True),
            "nombre": st.column_config.TextColumn("Nombre"),
            "sucursal": st.column_config.SelectboxColumn("Sucursal", options=[""]+SUCURSALES, required=False),
            "asesor": st.column_config.TextColumn("Asesor"),
            "fecha_ingreso": st.column_config.TextColumn("Fecha ingreso (YYYY-MM-DD)"),
            "fecha_dispersion": st.column_config.TextColumn("Fecha dispersión (YYYY-MM-DD)"),
            "estatus": st.column_config.SelectboxColumn("Estatus", options=ESTATUS_OPCIONES, required=True),
            "monto_propuesta": st.column_config.TextColumn("Monto propuesta"),
            "monto_final": st.column_config.TextColumn("Monto final"),
            "segundo_estatus": st.column_config.SelectboxColumn("Segundo estatus", options=SEGUNDO_ESTATUS_OPCIONES),
            "observaciones": st.column_config.TextColumn("Observaciones"),
            "score": st.column_config.TextColumn("Score"),
            "telefono": st.column_config.TextColumn("Teléfono"),
            "correo": st.column_config.TextColumn("Correo"),
            "analista": st.column_config.TextColumn("Analista"),
            "fuente": st.column_config.TextColumn("Fuente"),
        }

        df_clientes_mostrar["sucursal"] = df_clientes_mostrar["sucursal"].where(df_clientes_mostrar["sucursal"].isin(SUCURSALES), "")
        # antes de mostrar el editor, ordenar df_clientes_mostrar por fechas asc
        df_clientes_mostrar = sort_df_by_dates(df_clientes_mostrar)  # apply ordering
        # FIX: data_editor no acepta ColumnDataKind.DATETIME si la columna está configurada como TextColumn.
        # Convertir las columnas de fecha a strings 'YYYY-MM-DD' para mantener compatibilidad con column_config.
        for _dcol in ("fecha_ingreso", "fecha_dispersion"):
            if _dcol in df_clientes_mostrar.columns:
                try:
                    df_clientes_mostrar[_dcol] = pd.to_datetime(df_clientes_mostrar[_dcol], errors="coerce").dt.date.astype(str).replace("NaT", "")
                except Exception:
                    df_clientes_mostrar[_dcol] = df_clientes_mostrar[_dcol].astype(str).fillna("")
        ed = st.data_editor(
            df_clientes_mostrar,
            use_container_width=True,
            hide_index=True,
            column_config=colcfg,
            key="editor_clientes"
        )

        st.markdown("### Cambio de estatus")
        # asegurar ids_quick esté siempre definido para evitar NameError si df_clientes_mostrar no tiene 'id' o no es DataFrame
        try:
            ids_quick = (df_clientes_mostrar["id"].tolist() if (isinstance(df_clientes_mostrar, pd.DataFrame) and "id" in df_clientes_mostrar.columns) else [])
            ids_quick = [x for x in ids_quick if str(x).strip()]
            try:
                ids_quick = sorted(ids_quick, key=lambda s: (len(str(s)), str(s)))
            except Exception:
                pass
        except Exception:
            ids_quick = []
        if ids_quick:
            col_q1, col_q2, col_q3, col_q4 = st.columns([2,2,2,3])
            with col_q1:
                cid_quick = st.selectbox("Cliente", ids_quick, format_func=lambda x: f"{x} - {get_nombre_by_id(x)}")
                nombre_q = get_nombre_by_id(cid_quick)
                estatus_actual = get_field_by_id(cid_quick, "estatus")
                seg_actual = get_field_by_id(cid_quick, "segundo_estatus")
            with col_q2:
                nuevo_estatus = st.selectbox("Nuevo estatus", ESTATUS_OPCIONES, index=ESTATUS_OPCIONES.index(estatus_actual) if estatus_actual in ESTATUS_OPCIONES else 0)
            with col_q3:
                nuevo_seg = st.selectbox("Segundo estatus", SEGUNDO_ESTATUS_OPCIONES, index=SEGUNDO_ESTATUS_OPCIONES.index(seg_actual) if seg_actual in SEGUNDO_ESTATUS_OPCIONES else 0)
            with col_q4:
                obs_q = st.text_input("Observaciones (opcional)")
                if st.button("Actualizar estatus"):
                    base = df_cli.set_index("id")
                    base.at[cid_quick, "estatus"] = nuevo_estatus
                    base.at[cid_quick, "segundo_estatus"] = nuevo_seg
                    df_cli = base.reset_index()
                    guardar_clientes(df_cli)
                    # registrar en historial quién hizo el cambio (modificar)
                    actor = (current_user() or {}).get("user") or (current_user() or {}).get("email")
                    append_historial(cid_quick, nombre_q, estatus_actual, nuevo_estatus, seg_actual, nuevo_seg, obs_q, action="ESTATUS MODIFICADO", actor=actor)
                    st.success(f"Estatus actualizado para {cid_quick} ✅")
                    do_rerun()

        col_save, col_del = st.columns([1,1])
        with col_save:
            if st.button("💾 Guardar cambios"):
                # conservar copia original para detectar cambios y registrar historial
                original_df = df_cli.copy()
                base = df_cli.set_index("id")
                for _, row in ed.iterrows():
                    cid = row["id"]
                    for k in COLUMNS:
                        if k == "id":
                            continue
                        base.at[cid, k] = str(row.get(k, ""))
                # NORMALIZAR/UNIFICAR asesores en el dataframe antes de guardar
                for idx in base.index:
                    base.at[idx, "asesor"] = find_matching_asesor(base.at[idx, "asesor"], base.reset_index())
                df_cli = base.reset_index()
                # registrar en historial los cambios por fila (si hay diferencias relevantes)
                try:
                    actor = (current_user() or {}).get("user") or (current_user() or {}).get("email")
                    for idx in df_cli.index:
                        cid = df_cli.at[idx, "id"]
                        old_row = original_df[original_df["id"] == cid]
                        if not old_row.empty:
                            old_row = old_row.iloc[0]
                            # comparar estatus y segundo estatus y también detectar cambios en otras columnas
                            diffs = []
                            for c in COLUMNS:
                                if c == "id":
                                    continue
                                oldv = str(old_row.get(c, ""))
                                newv = str(df_cli.at[idx, c])
                                if oldv != newv:
                                    diffs.append(c)
                            if diffs:
                                est_old = old_row.get("estatus", "")
                                est_new = df_cli.at[idx, "estatus"] if "estatus" in df_cli.columns else ""
                                seg_old = old_row.get("segundo_estatus", "")
                                seg_new = df_cli.at[idx, "segundo_estatus"] if "segundo_estatus" in df_cli.columns else ""
                                obs = "Campos cambiados: " + ",".join(diffs)
                                append_historial(cid, df_cli.at[idx, "nombre"], est_old, est_new, seg_old, seg_new, obs, action="ESTATUS MODIFICADO", actor=actor)
                except Exception:
                    pass

                guardar_clientes(df_cli)
                st.success("Cambios guardados ✅")
                # Forzar reconstrucción de filtros de asesores en el sidebar
                try:
                    for _k in ("f_ases", "f_ases_ms", "f_ases_all"):
                        st.session_state.pop(_k, None)
                    st.session_state["_filters_token"] = st.session_state.get("_filters_token", 0) + 1
                except Exception:
                    pass
                do_rerun()

        with col_del:
            st.caption("Eliminar cliente (Siempre dar doble click para confirmar)")
            
            if can("delete_client"):
                    if ids_quick:
                        # mostrar opciones con 'ID - Nombre' para permitir borrar por nombre visualmente
                        opts = [""] + [f"{cid} - {get_nombre_by_id(cid)}" if get_nombre_by_id(cid) else str(cid) for cid in ids_quick]
                        sel = st.selectbox("Cliente a eliminar (ID - Nombre)", opts)
                        # extraer id del texto seleccionado
                        cid_del = ""
                        if sel:
                            if " - " in sel:
                                cid_del = sel.split(" - ", 1)[0]
                            else:
                                cid_del = sel
                    if cid_del and st.button("🗑️ Eliminar seleccionado"):
                        # registrar antes de eliminar
                        try:
                            nombre_del = get_nombre_by_id(cid_del)
                        except Exception:
                            nombre_del = ""
                        actor = (current_user() or {}).get("user") or (current_user() or {}).get("email")
                        append_historial(cid_del, nombre_del, "", "", "", "", f"Eliminado por {actor}", action="CLIENTE ELIMINADO", actor=actor)
                        df_cli = eliminar_cliente(cid_del, df_cli, borrar_historial=False)
                        st.success(f"Cliente {cid_del} eliminado ✅")
                        do_rerun()
            else:
                st.info("No tienes permiso para eliminar clientes.")

# ===== Asesores (conteo + descarga Excel) =====
with tab_asesores:
    st.subheader("👥 Dashboard por asesor")
    
    # ---------- TAB: ASESORES ----------
    # CAMBIO: Mostrar TODOS los clientes sin aplicar filtros del sidebar
    # igual que en la pestaña de clientes
    try:
        _df_all = cargar_y_corregir_clientes()  # Usar la función que carga datos frescos
        
        # Mostrar información como toasts temporales
        st.toast(f"📊 Total de registros cargados: **{len(_df_all)}**", icon="📊")
        if not _df_all.empty:
            asesores_unicos = sorted(_df_all['asesor'].fillna('(Sin asesor)').unique().tolist())
            st.toast(f"👥 Asesores únicos encontrados: **{', '.join(asesores_unicos)}**", icon="👥")
            
        # CAMBIO: NO aplicar ningún filtro del sidebar - mostrar todos los clientes
        base_ases = _df_all.copy()
        
        st.toast(f"✅ Mostrando TODOS los registros (sin filtros): **{len(base_ases)}**", icon="✅")
            
    except Exception as e:
        # Fallback: usar df_cli completo si algo falla
        st.error(f"❌ Error en pestaña asesores: {str(e)}")
        base_ases = df_cli.copy()
    
    # ===== FILTROS ESPECÍFICOS PARA LA PESTAÑA DE ASESORES =====
    st.markdown("---")
    
    # Crear opciones para los filtros basadas en los datos cargados
    if not base_ases.empty:
        # Preparar opciones de filtros
        sucursal_for_ases = base_ases["sucursal"].fillna("").replace({"": "(Sin sucursal)"})
        SUC_ASES_ALL = sorted(list(dict.fromkeys(sucursal_for_ases.unique().tolist())))
        
        asesor_for_ases = base_ases["asesor"].fillna("").replace({"": "(Sin asesor)"})
        ASES_ASES_ALL = sorted(list(dict.fromkeys(asesor_for_ases.unique().tolist())))
        
        estatus_for_ases = base_ases["estatus"].fillna("").unique().tolist()
        EST_ASES_ALL = sorted([e for e in estatus_for_ases if e])
        
        fuente_for_ases = base_ases["fuente"].fillna("").replace({"": "(Sin fuente)"})
        FUENTE_ASES_ALL = sorted(list(dict.fromkeys(fuente_for_ases.unique().tolist())))
        
        # Contenedor con estilo para filtros
        with st.container():
            # Encabezado de filtros con botón de reset
            col_header, col_reset_btn = st.columns([4, 1])
            with col_header:
                st.markdown("### 🔍 Filtros de Búsqueda")
                st.caption("Refina tu búsqueda usando los filtros disponibles")
            with col_reset_btn:
                st.write("")  # Espaciado
                if st.button("🔄 Resetear", key="reset_ases_filters", use_container_width=True):
                    st.session_state["_reset_ases_filters"] = True
                    st.rerun()
            
            # Manejar reset si el flag está activo
            if st.session_state.get("_reset_ases_filters", False):
                st.session_state["_reset_ases_filters"] = False
                keys_to_reset = ["ases_filter_suc", "ases_filter_asesor", "ases_filter_est", "ases_filter_fuente", "ases_filter_individual"]
                for key in keys_to_reset:
                    if key in st.session_state:
                        del st.session_state[key]
                st.rerun()
            
            st.markdown("---")
            
            # FILTRO DESTACADO: Asesor Individual (más usado)
            st.markdown("#### 🎯 Búsqueda Rápida por Asesor")
            col_individual, col_spacer = st.columns([3, 1])
            with col_individual:
                try:
                    current_individual = st.session_state.get("ases_filter_individual", "(Todos)")
                    options_list = ["(Todos)"] + ASES_ASES_ALL
                    if current_individual in options_list:
                        default_index = options_list.index(current_individual)
                    else:
                        default_index = 0
                except:
                    default_index = 0
                    
                asesor_individual = st.selectbox(
                    "Selecciona un asesor específico o 'Todos' para filtros avanzados:",
                    ["(Todos)"] + ASES_ASES_ALL,
                    index=default_index,
                    key="ases_filter_individual",
                    label_visibility="collapsed"
                )
            
            # FILTROS AVANZADOS (en expander cuando "Todos" está seleccionado)
            if asesor_individual == "(Todos)":
                with st.expander("⚙️ Filtros Avanzados", expanded=True):
                    st.markdown("**Combina múltiples criterios de búsqueda:**")
                    
                    # Primera fila de filtros
                    col_f1, col_f2 = st.columns(2)
                    
                    with col_f1:
                        st.markdown("##### 🏢 Sucursales")
                        f_ases_suc = st.multiselect(
                            "Filtrar por sucursales",
                            SUC_ASES_ALL,
                            default=st.session_state.get("ases_filter_suc", SUC_ASES_ALL),
                            key="ases_filter_suc",
                            label_visibility="collapsed",
                            help="Selecciona una o más sucursales"
                        )
                        st.caption(f"✓ {len(f_ases_suc)} de {len(SUC_ASES_ALL)} seleccionadas")
                    
                    with col_f2:
                        st.markdown("##### 👥 Asesores")
                        f_ases_asesor = st.multiselect(
                            "Filtrar por asesores",
                            ASES_ASES_ALL,
                            default=st.session_state.get("ases_filter_asesor", ASES_ASES_ALL),
                            key="ases_filter_asesor",
                            label_visibility="collapsed",
                            help="Selecciona uno o más asesores"
                        )
                        st.caption(f"✓ {len(f_ases_asesor)} de {len(ASES_ASES_ALL)} seleccionados")
                    
                    # Segunda fila de filtros
                    col_f3, col_f4 = st.columns(2)
                    
                    with col_f3:
                        st.markdown("##### 📊 Estatus")
                        f_ases_est = st.multiselect(
                            "Filtrar por estatus",
                            EST_ASES_ALL,
                            default=st.session_state.get("ases_filter_est", EST_ASES_ALL),
                            key="ases_filter_est",
                            label_visibility="collapsed",
                            help="Selecciona uno o más estatus"
                        )
                        st.caption(f"✓ {len(f_ases_est)} de {len(EST_ASES_ALL)} seleccionados")
                    
                    with col_f4:
                        st.markdown("##### 📢 Fuentes")
                        f_ases_fuente = st.multiselect(
                            "Filtrar por fuentes",
                            FUENTE_ASES_ALL,
                            default=st.session_state.get("ases_filter_fuente", FUENTE_ASES_ALL),
                            key="ases_filter_fuente",
                            label_visibility="collapsed",
                            help="Selecciona una o más fuentes de captación"
                        )
                        st.caption(f"✓ {len(f_ases_fuente)} de {len(FUENTE_ASES_ALL)} seleccionadas")
            else:
                # Si hay un asesor individual seleccionado, usar todos los valores por defecto
                f_ases_suc = SUC_ASES_ALL
                f_ases_asesor = ASES_ASES_ALL
                f_ases_est = EST_ASES_ALL
                f_ases_fuente = FUENTE_ASES_ALL

        # Aplicar filtros específicos de la pestaña de asesores
        try:
            # Filtro por sucursal
            if f_ases_suc and len(f_ases_suc) < len(SUC_ASES_ALL):
                suc_mask_ases = sucursal_for_ases.isin(f_ases_suc)
            else:
                suc_mask_ases = pd.Series(True, index=base_ases.index)
            
            # Filtro por asesor (multiselect)
            if f_ases_asesor and len(f_ases_asesor) < len(ASES_ASES_ALL):
                asesor_mask_ases = asesor_for_ases.isin(f_ases_asesor)
            else:
                asesor_mask_ases = pd.Series(True, index=base_ases.index)
            
            # Filtro individual de asesor (selectbox) - tiene prioridad si se selecciona
            if asesor_individual and asesor_individual != "(Todos)":
                asesor_individual_mask = asesor_for_ases == asesor_individual
            else:
                asesor_individual_mask = pd.Series(True, index=base_ases.index)
            
            # Filtro por estatus
            if f_ases_est and len(f_ases_est) < len(EST_ASES_ALL):
                est_mask_ases = base_ases["estatus"].isin(f_ases_est)
            else:
                est_mask_ases = pd.Series(True, index=base_ases.index)
            
            # Filtro por fuente
            if f_ases_fuente and len(f_ases_fuente) < len(FUENTE_ASES_ALL):
                fuente_mask_ases = fuente_for_ases.isin(f_ases_fuente)
            else:
                fuente_mask_ases = pd.Series(True, index=base_ases.index)
            
            # Aplicar todos los filtros (individual de asesor tiene prioridad)
            base_ases = base_ases[suc_mask_ases & asesor_mask_ases & asesor_individual_mask & est_mask_ases & fuente_mask_ases].copy()
            
            # Mostrar información de resultados
            if asesor_individual and asesor_individual != "(Todos)":
                st.info(f"🎯 Mostrando solo: **{asesor_individual}** - **{len(base_ases)}** registros")
            else:
                st.info(f"📋 Registros después de filtros: **{len(base_ases)}** de **{len(_df_all)}** totales")
        
        except Exception as e:
            st.warning(f"Error aplicando filtros: {e}")
    
    st.markdown("---")
 
    # Si no hay datos tras filtros, informar y continuar (mostrar tarjetas vacías)
    if base_ases.empty:
        st.info("No hay clientes que coincidan con los filtros actuales.")
    else:
        # --- Filtro por rango de fechas (opcional) aplicado sobre la base filtrada ---
        date_col = None
        for c in ("fecha_ingreso", "fecha_dispersion"):
            if c in base_ases.columns:
                date_col = c
                break

        if date_col is not None:
            try:
                # Usar fechas de TODOS los datos para establecer el rango
                base_ases[date_col] = pd.to_datetime(base_ases[date_col], errors="coerce")
                min_date = base_ases[date_col].min()
                max_date = base_ases[date_col].max()
                if not pd.isna(min_date) and not pd.isna(max_date):
                    default_start = min_date.date()
                    default_end = max_date.date()
                    dr = st.date_input("Filtrar por fecha (desde → hasta)", value=(default_start, default_end), key="asesores_date_range")
                    start_date, end_date = dr if isinstance(dr, tuple) else (dr, dr)
                    if start_date and end_date:
                        # Aplicar filtro de fecha sobre base_ases
                        mask_date = base_ases[date_col].dt.date
                        base_ases = base_ases[mask_date.between(start_date, end_date)]
                else:
                    st.info("No hay valores de fecha válidos para filtrar en la base de asesores.")
            except Exception:
                pass

        # Reemplaza vacío por '(Sin asesor)' solo para mostrar
        tmp = base_ases.assign(_asesor=base_ases["asesor"].replace("", "(Sin asesor)"))

        # Conteo por asesor (para tarjetas/lista)
        conteo_por_asesor = (
            tmp.groupby("_asesor", dropna=False)["id"]
               .count()
               .reset_index(name="conteo")
               .rename(columns={"_asesor": "asesor"})
               .sort_values(["asesor"])
        )

        # Conteo por asesor x estatus (para tabla o grid)
        df_agrupe = (
            tmp.groupby(["_asesor", "estatus"], dropna=False)
               .size()
               .reset_index(name="conteo")
               .rename(columns={"_asesor": "asesor"})
               .sort_values(["asesor", "estatus"])
        )
        col_l, col_r = st.columns([2, 3])

        with col_l:
            st.markdown("**Conteo por asesor**")
            st.dataframe(conteo_por_asesor, use_container_width=True, hide_index=True)

            # REMOVED: selector adicional de Asesor (ahora lo controla la sidebar)
            st.markdown("**Detalle de clientes (filtrados)**")
            # Mostrar el detalle real de clientes filtrados (usar la base filtrada, no el dataframe agregado)
            # Seleccionar solo las columnas de COLUMNS que realmente existen en base_ases para evitar KeyError
            cols_present = [c for c in COLUMNS if c in base_ases.columns]
            if cols_present:
                df_detalle_for_view = base_ases.loc[:, cols_present].copy()
            else:
                # fallback: mostrar todas las columnas disponibles si ninguna de COLUMNS está presente
                df_detalle_for_view = base_ases.copy()
            df_detalle_for_view = sort_df_by_dates(df_detalle_for_view)
            st.dataframe(df_detalle_for_view, use_container_width=True, hide_index=True)

            # ---- Descargas en Excel ----
            import io
            import pandas as pd

            def build_excel_bytes(df_dict):
                bio = io.BytesIO()
                engine = None
                # Prefer xlsxwriter, fallback a openpyxl si no está
                try:
                    import xlsxwriter  # type: ignore
                    engine = "xlsxwriter"
                except Exception:
                    try:
                        import openpyxl  # type: ignore
                        engine = "openpyxl"
                    except Exception:
                        engine = None

                if engine is None:
                    st.warning("No se encontró 'xlsxwriter' ni 'openpyxl'. Instala uno de ellos (pip install openpyxl) para habilitar descargas XLSX.")
                    return None

                with pd.ExcelWriter(bio, engine=engine) as writer:
                    for sheet_name, dfx in df_dict.items():
                        sheet = sheet_name[:31] if sheet_name else "hoja"
                        dfx.to_excel(writer, index=False, sheet_name=sheet)
                bio.seek(0)
                return bio

            # (a) Excel de los filtrados (una hoja "Filtrados")
            # Usar la base de clientes filtrada (tmp) en lugar del dataframe agregado df_agrupe
            cols_present = [c for c in COLUMNS if c in tmp.columns]
            if not cols_present:
                cols_present = list(tmp.columns)
            xls_sel = build_excel_bytes({"Filtrados": sort_df_by_dates(tmp[cols_present].copy())})
            if xls_sel is not None:
                if st.download_button(
                    "⬇️ Descargar Excel (filtrados)",
                    data=xls_sel,
                    file_name="clientes_asesores_filtrados.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    key=f"dl_xls_asesor_sel"
                ):
                    try:
                        actor = (current_user() or {}).get("user") or (current_user() or {}).get("email")
                        append_historial(
                            "",  # no es por cliente específico
                            "",  # no hay nombre de cliente
                            "", "",
                            "", "",
                            "Descarga de Excel (clientes filtrados)",
                            action="DESCARGA ZIP ASESOR", 
                            actor=actor
                        )
                    except Exception:
                        pass
            else:
                st.info("Descarga XLSX deshabilitada hasta instalar openpyxl o xlsxwriter.")

            # (b) Un Excel con una hoja por asesor (solo los filtrados)
            hojas = {}
            # Crear una hoja por asesor usando las filas reales de clientes (tmp)
            for a in conteo_por_asesor["asesor"].tolist():
                try:
                    dfx = tmp[tmp["_asesor"] == a].copy()
                    cols_present = [c for c in COLUMNS if c in dfx.columns]
                    if not cols_present:
                        cols_present = list(dfx.columns)
                    hojas[a] = sort_df_by_dates(dfx.loc[:, cols_present].copy())
                except Exception:
                    hojas[a] = sort_df_by_dates(dfx.copy() if 'dfx' in locals() else tmp.copy())
            if hojas:
                xls_all = build_excel_bytes(hojas)
                if xls_all is not None:
                    if st.download_button(
                        "⬇️ Descargar Excel (una hoja por asesor)",
                        data=xls_all,
                        file_name="clientes_por_asesor_filtrados.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                        key="dl_xls_asesores_todos"
                    ):
                        try:
                            actor = (current_user() or {}).get("user") or (current_user() or {}).get("email")
                            append_historial(
                                "", "", "", "", "", "",
                                "Descarga de Excel (hojas por asesor)",
                                action="DESCARGA ZIP ASESOR",  # o "DOCUMENTOS", según quieras categorizarlo
                                actor=actor
                            )
                        except Exception:
                            pass
                else:
                    st.info("Descarga XLSX deshabilitada hasta instalar openpyxl o xlsxwriter.")
        with col_r:
            st.markdown("**Gráfica: clientes por asesor**")
            try:
                # Preparar datos y dimensiones usando la columna 'conteo' (número de clientes)
                df_plot = conteo_por_asesor.copy()
                df_plot["asesor"] = df_plot["asesor"].astype(str)
                maxv = int(df_plot["conteo"].max() if not df_plot.empty else 0)
                n_ases = len(df_plot)
                height_px = max(240, n_ases * 42)

                # Gráfica horizontal simple y robusta (usa 'conteo'):
                bars = (
                    alt.Chart(df_plot)
                    .mark_bar(color="#4c78a8", cornerRadius=4)
                    .encode(
                        x=alt.X(
                            "conteo:Q",
                            axis=alt.Axis(format="d", title="Clientes"),
                            scale=alt.Scale(domain=[0, maxv * 1.15 if maxv > 0 else 1])
                        ),
                        y=alt.Y(
                            "asesor:N",
                            sort=alt.EncodingSortField(field="conteo", order="descending"),
                            title="Asesor"
                        ),
                        tooltip=[alt.Tooltip("asesor:N"), alt.Tooltip("conteo:Q", format="d")]
                    )
                )

                # Etiquetas con el conteo al final de cada barra
                labels = (
                    alt.Chart(df_plot)
                    .mark_text(align="left", dx=6, color="black", fontSize=11)
                    .encode(
                        x=alt.X("conteo:Q"),
                        y=alt.Y("asesor:N", sort=alt.EncodingSortField(field="conteo", order="descending")),
                        text=alt.Text("conteo:Q", format="d")
                    )
                )

                st.altair_chart((bars + labels).properties(height=height_px), use_container_width=True)
            except Exception as e:
                st.warning("No se pudo renderizar la gráfica.")
                st.error(str(e))

        # ---- Tabla pivote por estatus (opcional, útil para seguimiento) ----
        st.markdown("---")
        st.markdown("**Distribución por estatus y asesor (filtrados)**")
        # Usar la columna 'conteo' del df_agrupe (que es el conteo por asesor x estatus)
        piv = (
            df_agrupe
            .pivot_table(index="asesor", columns="estatus", values="conteo", aggfunc="sum", fill_value=0)
            .reset_index()
        )
        st.dataframe(piv, use_container_width=True, hide_index=True)
# ===== Documentos (por cliente) =====
# Safety: garantizar que las pestañas fueron creadas; si no, volver a crearlas para evitar NameError.
if 'tab_docs' not in globals():
    tab_dash, tab_cli, tab_docs, tab_import, tab_hist, tab_asesores = st.tabs(
        ["📊 Dashboard", "📋 Clientes", "📎 Documentos", "📥 Importar", "🗂️ Historial", " 👥 Asesores"]
    )

with tab_docs:
    st.subheader("📎 Documentos por cliente")
    # Cargar datos frescos para la pestaña de documentos
    df_cli = cargar_y_corregir_clientes()
    if df_cli.empty:
        st.info("No hay clientes aún.")
    else:
        ids = (df_cli["id"].tolist() if (isinstance(df_cli, pd.DataFrame) and "id" in df_cli.columns) else [])
        ids = [x for x in ids if str(x).strip()]
        try:
            ids = sorted(ids, key=lambda s: (len(str(s)), str(s)))
        except Exception:
            pass
        cid_sel = st.selectbox(
            "Selecciona cliente",
            [""] + ids,
            format_func=lambda x: "—" if x == "" else f"{x} - {get_nombre_by_id(x)}",
            key="docs_cid_sel"
        )
        if cid_sel:
            estatus_cliente_sel = get_field_by_id(cid_sel, "estatus")
            st.markdown("#### Subir documentos")
            # Unificar los uploaders en un solo formulario con un botón "Subir archivos"
            form_key = f"form_subir_docs_{cid_sel}"
            with st.form(form_key, clear_on_submit=True):
                up_estado_e = st.file_uploader("Estado de cuenta", type=DOC_CATEGORIAS["estado_cuenta"], accept_multiple_files=True, key=f"estado_{cid_sel}")
                up_buro_e = st.file_uploader("Buró de crédito", type=DOC_CATEGORIAS["buro_credito"], accept_multiple_files=True, key=f"buro_{cid_sel}")
                up_solic_e = st.file_uploader("Solicitud", type=DOC_CATEGORIAS["solicitud"], accept_multiple_files=True, key=f"solic_{cid_sel}")
                up_otros_e = st.file_uploader("Otros", type=DOC_CATEGORIAS["otros"], accept_multiple_files=True, key=f"otros_{cid_sel}")
                if _is_dispersion(estatus_cliente_sel):
                    up_contrato_e = st.file_uploader("Contrato ", type=DOC_CATEGORIAS["contrato"], accept_multiple_files=True, key=f"contrato_{cid_sel}")
                else:
                    up_contrato_e = None
                submitted = st.form_submit_button("⬆️ Subir archivos")
                if submitted:
                    subidos_lote = []
                    if up_estado_e:   subidos_lote += subir_docs(cid_sel, up_estado_e,   prefijo="estado_")
                    if up_buro_e:     subidos_lote += subir_docs(cid_sel, up_buro_e,     prefijo="buro_")
                    if up_solic_e:    subidos_lote += subir_docs(cid_sel, up_solic_e,    prefijo="solic_")
                    if up_otros_e:    subidos_lote += subir_docs(cid_sel, up_otros_e,    prefijo="otros_")
                    if up_contrato_e: subidos_lote += subir_docs(cid_sel, up_contrato_e, prefijo="contrato_")

                    if subidos_lote:
                        # Limpia uploaders
                        for k in (f"estado_{cid_sel}", f"buro_{cid_sel}", f"solic_{cid_sel}", f"otros_{cid_sel}", f"contrato_{cid_sel}"):
                            st.session_state.pop(k, None)

                        # 1 sola línea en historial
                        actor = (current_user() or {}).get("user") or (current_user() or {}).get("email")
                        try:
                            nombre_x = get_nombre_by_id(cid_sel)
                            est_x    = get_field_by_id(cid_sel, "estatus")
                            seg_x    = get_field_by_id(cid_sel, "segundo_estatus")
                        except Exception:
                            nombre_x = est_x = seg_x = ""

                        append_historial(
                            str(cid_sel), nombre_x,
                            est_x, est_x, seg_x, seg_x,
                            f"Subidos: {', '.join(subidos_lote)}",
                            action="DOCUMENTOS", actor=actor
                        )

                        # refresco inmediato (token)
                        tok_key = f"docs_token_{cid_sel}"
                        st.session_state[tok_key] = st.session_state.get(tok_key, 0) + 1
                        st.success(f"Archivo(s) subido(s): {len(subidos_lote)} ✅")
                    else:
                        st.info("No seleccionaste archivos para subir.")

            st.markdown("—")
            if _is_dispersion(estatus_cliente_sel):
                st.success("Estatus actual: DISPERSADO — sube el Contrato en el formulario de arriba.")
            else:
                st.info("Para subir el Contrato, cambia el estatus del cliente a **en dispersión**.")

            # token para forzar re-render de botones de descarga cuando haya uploads
            tok_key = f"docs_token_{cid_sel}"
            tok = st.session_state.get(tok_key, 0)

            files = listar_docs_cliente(cid_sel)
            if files:
                st.markdown("#### Archivos del cliente")
                # mapping explícito de prefijos usados al guardar
                prefix_map = {
                    "estado_cuenta": "estado_",
                    "buro_credito": "buro_",
                    "solicitud": "solic_",
                    "contrato": "contrato_",
                    "otros": "otros_",
                }
                for cat in DOC_CATEGORIAS.keys():
                    pref = prefix_map.get(cat, cat.split('_')[0] + "_")
                    cat_files = [f for f in files if f.name.startswith(pref)]
                    if cat_files:
                        st.write(f"• {cat.replace('_',' ').title()}:")
                        for f in cat_files:
                                    # Flow: user clicks a request button which prepares the bytes and
                                    # registers the download in historial; then a download_button
                                    # appears where the user can complete the download.
                                    req_key = f"dl_req_{cid_sel}_{tok}_{f.name}"
                                    blob_key = f"dl_blob_{cid_sel}_{f.name}"
                                    btn_label = f"{f.name}"
                                    #if st.button(btn_label, key=req_key):
                                    try:
                                        data_bytes = f.read_bytes()
                                    except Exception:
                                        data_bytes = b""

                                    if st.download_button(
                                        f"⬇️Descargar {f.name}",
                                        data=data_bytes,
                                        file_name=f.name,
                                        key=f"dl_btn_{cid_sel}_{tok}_{f.name}"
                                    ):
                                            # Registrar en historial la descarga
                                        try:
                                            nombre_x = get_nombre_by_id(cid_sel)
                                            est_x    = get_field_by_id(cid_sel, "estatus")
                                            seg_x    = get_field_by_id(cid_sel, "segundo_estatus")
                                        except Exception:
                                            nombre_x = est_x = seg_x = ""
                                        actor = (current_user() or {}).get("user") or (current_user() or {}).get("email")
                                        append_historial(
                                            str(cid_sel), nombre_x,
                                            est_x, est_x, seg_x, seg_x,
                                            f"Descargado: {f.name}",
                                            action="DESCARGA DOCUMENTO",   # o el que uses en ACTION_LABELS
                                            actor=actor
                                        )


                                    # --- Acciones adicionales: Eliminar / Reemplazar ---
                                    a1, a2 = st.columns([1, 2])
                                    with a1:
                                        del_key = f"del_file_{cid_sel}_{f.name}"
                                        if st.button("Eliminar", key=del_key):
                                            try:
                                                # borrar archivo físico
                                                f.unlink()
                                                # limpiar blobs relacionados
                                                st.session_state.pop(blob_key, None)
                                                # forzar refresh de botones
                                                st.session_state[tok_key] = st.session_state.get(tok_key, 0) + 1
                                                # historial
                                                try:
                                                    actor = (current_user() or {}).get("user") or (current_user() or {}).get("email")
                                                    append_historial(str(cid_sel), get_nombre_by_id(cid_sel), "", "", "", "", f"Eliminado: {f.name}", action="DOCUMENTOS", actor=actor)
                                                except Exception:
                                                    pass
                                                st.success(f"Archivo eliminado: {f.name}")
                                            except Exception as e:
                                                st.error(f"No se pudo eliminar {f.name}: {e}")

                            
                # Después de listar todas las categorías, ofrecer ZIP del cliente (una sola vez)
                if st.button("📦 Descargar carpeta (ZIP)", key=f"zip_cliente_{cid_sel}"):
                    zip_buffer = io.BytesIO()
                    with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zf:
                        for f in files:
                            if f.is_file():
                                zf.write(f, arcname=f.name)
                    zip_buffer.seek(0)
                    # registrar en historial la descarga del ZIP del cliente
                    try:
                        actor = (current_user() or {}).get("user") or (current_user() or {}).get("email")
                        append_historial(str(cid_sel), get_nombre_by_id(cid_sel), "", "", "", "", f"ZIP cliente preparado ({len(files)} archivos)", action="DESCARGA ZIP CLIENTE", actor=actor)
                    except Exception:
                        pass
                    st.session_state[f"_last_zip_{cid_sel}"] = zip_buffer.getvalue()
                if st.session_state.get(f"_last_zip_{cid_sel}"):
                    st.download_button(
                        "⬇️ Descargar ZIP del cliente",
                        data=st.session_state.get(f"_last_zip_{cid_sel}"),
                        file_name=f"{safe_name(cid_sel)}_{safe_name(get_nombre_by_id(cid_sel))}.zip",
                        mime="application/zip",
                        key=f"dl_zip_cliente_{cid_sel}"
                    )
            else:
                st.info("Este cliente no tiene documentos.")

            if can("delete_client"):
                st.markdown("---")
                st.error("⚠️ Eliminar cliente (borra su carpeta y su historial).")
                st.caption("Siempre dar doble click para confirmar.")
                if st.button(f"🗑️ Eliminar {cid_sel}", key=f"del_{cid_sel}"):
                    # registrar en historial antes de eliminar
                    nombre_del = get_nombre_by_id(cid_sel)
                    actor = (current_user() or {}).get("user") or (current_user() or {}).get("email")
                    append_historial(cid_sel, nombre_del, "", "", "", "", f"Eliminado por {actor}", action="CLIENTE ELIMINADO", actor=actor)
                    df_cli = eliminar_cliente(cid_sel, df_cli, borrar_historial=False)
                    st.success(f"Cliente {cid_sel} eliminado ✅")
                    do_rerun()
            else:
                st.info("Solo el administrador puede eliminar clientes.")

# ===== Importar (SOLO Excel) =====  # NEW: ZIP eliminado
with tab_import:
    st.subheader("📥 Importar clientes desde Excel (.xlsx)")
    st.caption("Descarga la plantilla, mapea columnas y ejecuta la importación.")

    import_cols_required = [
        "nombre","sucursal","asesor","fecha_ingreso","fecha_dispersion",
        "estatus","monto_propuesta","monto_final","segundo_estatus",
        "observaciones","score","telefono","correo","analista"
    ]
    import_cols_optional = ["id", "fuente"]  # si viene, permite actualizar por ID

    cta1, cta2 = st.columns([1,3])
    with cta1:
        st.caption("Plantilla de importación deshabilitada.")

    def _read_excel_uploaded(file) -> pd.DataFrame:
        try:
            df = pd.read_excel(file, dtype=str).fillna("")
            if sum(str(c).startswith("Unnamed") for c in df.columns) > len(df.columns) * 0.6:
                headers = [str(x).strip() for x in df.iloc[0].tolist()]
                df = df.iloc[1:].copy()
                df.columns = headers
            df.columns = [str(c).strip() for c in df.columns]
            return df
        except Exception as e:
            st.error(f"Error leyendo Excel: {e}")
            return pd.DataFrame()

    up_excel = st.file_uploader("Sube tu Excel (.xlsx)", type=["xlsx"], accept_multiple_files=False, key="up_excel_main")

    if up_excel:
        df_imp_raw = _read_excel_uploaded(up_excel)
        if df_imp_raw.empty:
            st.warning("El Excel está vacío o no se pudo leer.")
        else:
            with st.expander("Vista previa", expanded=True):
                st.dataframe(sort_df_by_dates(df_imp_raw).head(10), use_container_width=True)

            st.markdown("#### Mapeo de columnas")
            df_cols = df_imp_raw.columns.tolist()
            mapping = {}
            map_cols = import_cols_optional + import_cols_required
            M1, M2, M3 = st.columns(3)
            for i, col_needed in enumerate(map_cols):
                col = [M1, M2, M3][i % 3]
                mapping[col_needed] = col.selectbox(
                    f"Excel → {col_needed}",
                    ["(no asignar)"] + df_cols,
                    index=(df_cols.index(col_needed) + 1) if col_needed in df_cols else 0,
                    key=f"map_{col_needed}"
                )

            def _build_norm_df(df_src, mp):
                out = pd.DataFrame()
                for k in map_cols:
                    src = mp.get(k)
                    if src and src != "(no asignar)" and src in df_src.columns:
                        out[k] = df_src[src].astype(str).fillna("")
                    else:
                        out[k] = ""
                return out

            df_norm = _build_norm_df(df_imp_raw, mapping)

            # --- Canonizar valores frente a catálogos existentes para evitar duplicados parecidos ---
            ESTATUS_SYNONYMS = {
                "en revision": "EN REVISIÓN",
                "en revisión": "EN REVISIÓN",
                "revision": "EN REVISIÓN",
                "revisión": "EN REVISIÓN",
            }
            SEGUNDO_ESTATUS_SYNONYMS = {
                # agrega sinónimos si los conoces
            }

            def _canon_est(x: str) -> str:
                try:
                    return canonicalize_from_catalog(x, ESTATUS_OPCIONES, extra_synonyms=ESTATUS_SYNONYMS, min_ratio=0.90)
                except Exception:
                    return x

            def _canon_seg(x: str) -> str:
                try:
                    return canonicalize_from_catalog(x, SEGUNDO_ESTATUS_OPCIONES, extra_synonyms=SEGUNDO_ESTATUS_SYNONYMS, min_ratio=0.90)
                except Exception:
                    return x

            def _canon_suc(x: str) -> str:
                try:
                    return canonicalize_from_catalog(x, SUCURSALES, extra_synonyms=None, min_ratio=0.92)
                except Exception:
                    return x

            for col, fn in [
                ("estatus", _canon_est),
                ("segundo_estatus", _canon_seg),
                ("sucursal", _canon_suc),
            ]:
                if col in df_norm.columns:
                    try:
                        df_norm[col] = df_norm[col].astype(str).map(fn)
                    except Exception:
                        df_norm[col] = df_norm[col]

            # Detectar nuevos valores que no estén en los catálogos actuales
            nuevas_suc = sorted(set(df_norm.loc[df_norm["sucursal"].ne(""), "sucursal"]) - set(SUCURSALES))
            nuevos_est = sorted(set(df_norm.loc[df_norm["estatus"].ne(""), "estatus"]) - set(ESTATUS_OPCIONES))
            nuevos_seg = sorted(set(df_norm.loc[df_norm["segundo_estatus"].ne(""), "segundo_estatus"]) - set(SEGUNDO_ESTATUS_OPCIONES))

            # Agregar automáticamente y persistir
            if nuevas_suc:
                SUCURSALES.extend([s for s in nuevas_suc if s.strip()])
                save_sucursales(SUCURSALES)
                st.info(f"Se agregaron {len(nuevas_suc)} sucursal(es): {', '.join(nuevas_suc)}")

            if nuevos_est:
                ESTATUS_OPCIONES.extend([e for e in nuevos_est if e.strip()])
                save_estatus(ESTATUS_OPCIONES)
                st.info(f"Se agregaron {len(nuevos_est)} estatus: {', '.join(nuevos_est)}")

            if nuevos_seg:
                SEGUNDO_ESTATUS_OPCIONES.extend([e for e in nuevos_seg if e.strip() or e == ""])
                save_segundo_estatus(SEGUNDO_ESTATUS_OPCIONES)
                st.info(f"Se agregaron {len(nuevos_seg)} segundo estatus: {', '.join([x if x else '(vacío)' for x in nuevos_seg])}")

            with st.expander("Previsualización mapeada", expanded=False):
                st.dataframe(sort_df_by_dates(df_norm).head(10), use_container_width=True)

            st.markdown("#### Modo de importación")
            modo = st.radio(
                "¿Cómo quieres importar?",
                ["Agregar (solo nuevos)", "Actualizar por ID (si coincide)", "Upsert por Nombre+Teléfono"],
                horizontal=True,
                key="modo_import"
            )

            # Normalizar fechas a str si vienen tipo fecha
            for fcol in ["fecha_ingreso","fecha_dispersion"]:
                try:
                    df_norm[fcol] = pd.to_datetime(df_norm[fcol], errors="ignore").astype(str).replace("NaT","")
                except Exception:
                    pass

        if st.button("🚀 Importar ahora", type="primary", key="btn_importar_2"):
            base = df_cli.copy()

            def _nuevo_id_local(df):
                base_id = 1000
                try:
                    if not df.empty and "id" in df.columns:
                        nums = []
                        for x in df["id"].astype(str):
                            if str(x).startswith("C"):
                                try:
                                    nums.append(int(str(x).lstrip("C")))
                                except Exception:
                                    continue
                        if nums:
                            base_id = max(nums) + 1
                        else:
                            base_id = base_id + len(df) + 1
                except Exception:
                    base_id = base_id + 1
                return f"C{base_id}"

            actualizados = 0
            agregados = 0

            df_norm_obj = locals().get('df_norm', None)
            if df_norm_obj is not None and (not getattr(df_norm_obj, 'empty', True)):
                for _, r in df_norm_obj.iterrows():
                    r = r.fillna("")
                    rid = str(r.get("id", "")).strip()
                    rnombre = str(r.get("nombre", "")).strip()
                    rtel = str(r.get("telefono", "")).strip()

                    idx = None
                    if modo == "Actualizar por ID (si coincide)" and rid:
                        hit = base.index[base["id"] == rid].tolist()
                        idx = hit[0] if hit else None
                    elif modo == "Upsert por Nombre+Teléfono" and rnombre and rtel:
                        hits = base.index[(base["nombre"] == rnombre) & (base["telefono"] == rtel)].tolist()
                        idx = hits[0] if hits else None

                    # construir registro y mapear asesor contra el base actual
                    registro = {k: str(r.get(k, "")) for k in COLUMNS if k != "id"}
                    registro["asesor"] = find_matching_asesor(registro.get("asesor", ""), base)

                    if idx is not None:
                        for k, v in registro.items():
                            base.at[idx, k] = v
                        actualizados += 1
                        try:
                            actor = (current_user() or {}).get("user") or (current_user() or {}).get("email")
                            cid_up = base.at[idx, "id"] if "id" in base.columns else (registro.get("id","") or "")
                            append_historial(cid_up, registro.get("nombre",""), "", registro.get("estatus",""), "", registro.get("segundo_estatus",""), f"Importación - actualizado", action="ESTATUS MODIFICADO", actor=actor)
                        except Exception:
                            pass
                    else:
                        if modo == "Agregar (solo nuevos)":
                            if rnombre and rtel and not base[(base["nombre"] == rnombre) & (base["telefono"] == rtel)].empty:
                                continue
                        new_id = rid if rid and (base["id"] != rid).all() else _nuevo_id_local(base)
                        nuevo = {"id": new_id, **registro}
                        base = pd.concat([base, pd.DataFrame([nuevo])], ignore_index=True)
                        agregados += 1
                        try:
                            actor = (current_user() or {}).get("user") or (current_user() or {}).get("email")
                            append_historial(new_id, nuevo.get("nombre",""), "", nuevo.get("estatus",""), "", nuevo.get("segundo_estatus",""), f"Importación - creado", action="CLIENTE AGREGADO", actor=actor)
                        except Exception:
                            pass

            try:
                base = _fix_missing_or_duplicate_ids(base)
            except Exception:
                pass
            guardar_clientes(base)
            st.success(f"Importación completada ✅  |  Agregados: {agregados}  ·  Actualizados: {actualizados}")

            # Limpieza del estado del mapeo para que no “se quede” la UI
            for k in list(st.session_state.keys()):
                if str(k).startswith("map_") or k in ("up_excel_main", "modo_import"):
                    st.session_state.pop(k, None)

            do_rerun()
        # (Se eliminó una copia duplicada del bloque "Historial de movimientos" aquí)
               
# ===== Historial =====
with tab_hist:
    # Mostrar el historial solo a administradores
    if not is_admin():
        st.warning("Solo los administradores pueden ver el historial.")
    else:
        st.subheader("🗂️ Historial de movimientos")
        try:
            dfh = cargar_historial()
        except Exception:
            dfh = pd.DataFrame()

        if dfh is None or dfh.empty:
            st.info("No hay registros en el historial.")
        else:
            # asegurarnos de tener columna de timestamp como datetime para ordenar
            try:
                dfh["_ts_dt"] = pd.to_datetime(dfh["ts"], errors="coerce")
                dfh = dfh.sort_values("_ts_dt", ascending=False)
                dfh = dfh.drop(columns=["_ts_dt"])
            except Exception:
                pass

            # Mostrar filtros simples
            cols_top = st.columns([3,2,2,2])
            with cols_top[0]:
                qid = st.text_input("Filtrar por ID de cliente (parcial)")
            with cols_top[1]:
                qactor = st.selectbox("Actor", ["TODOS"] + sorted([str(x) for x in sorted(set(dfh.get("actor",[])))]) , index=0)
            with cols_top[2]:
                # Etiquetas amigables para las acciones
                ACTION_LABELS = ["TODOS", "CLIENTE AGREGADO", "DESCARGA ZIP", "DESCARGA ZIP CLIENTE","DESCARGA ZIP ASESOR","DESCARGA DOCUMENTO", "DOCUMENTOS", "CLIENTE ELIMINADO", "ESTATUS MODIFICADO"]
                qaction = st.selectbox("Acción", ACTION_LABELS, index=0)
            with cols_top[3]:
                if st.button("Refrescar historial"):
                    # actualizar token en session_state para forzar recarga del CSV sin usar do_rerun()
                    st.session_state["hist_reload_token"] = st.session_state.get("hist_reload_token", 0) + 1
                    # al modificar session_state un widget hace rerun automático, no necesitamos do_rerun()

            df_show = dfh.copy()

            # --- Filtro por rango de fechas (columna 'ts') ---
            try:
                ts_all = pd.to_datetime(dfh.get('ts', pd.Series(dtype='object')), errors='coerce')
                if not ts_all.dropna().empty:
                    min_ts = ts_all.min()
                    max_ts = ts_all.max()
                    # rango por defecto: últimas 30 días o todo el rango si es menor
                    default_end = max_ts.date()
                    default_start = (max_ts - pd.Timedelta(days=30)).date() if (max_ts - pd.Timedelta(days=30)) > min_ts else min_ts.date()
                    dr = st.date_input("Filtrar historial por fecha (desde → hasta)", value=(default_start, default_end), key="hist_date_range")
                    start_date, end_date = (dr if isinstance(dr, tuple) else (dr, dr))
                    if start_date and end_date:
                        mask_dates = pd.to_datetime(df_show.get('ts', pd.Series(dtype='object')), errors='coerce').dt.date
                        df_show = df_show[mask_dates.between(start_date, end_date)]
            except Exception:
                pass
            if qid:
                df_show = df_show[df_show["id"].astype(str).str.contains(qid, case=False, na=False)]
            if qactor and qactor != "TODOS":
                df_show = df_show[df_show["actor"].astype(str) == qactor]
            if qaction and qaction != "TODOS":
                qa = qaction
                if qa == "CLIENTE AGREGADO":
                    df_show = df_show[df_show["action"].astype(str) == "CLIENTE AGREGADO"]
                elif qa == "CLIENTE ELIMINADO":
                    df_show = df_show[df_show["action"].astype(str) == "CLIENTE ELIMINADO"]
                elif qa == "ESTATUS MODIFICADO":
                    df_show = df_show[df_show["action"].astype(str) == "ESTATUS MODIFICADO"]
                elif qa == "DESCARGA ZIP":
                    df_show = df_show[df_show["action"].astype(str) == "DESCARGA ZIP"]
                elif qa == "DESCARGA ZIP CLIENTE":
                    df_show = df_show[df_show["action"].astype(str) == "DESCARGA ZIP CLIENTE"]
                elif qa == "DOCUMENTOS":
                    df_show = df_show[df_show["action"].astype(str) == "DOCUMENTOS"]
                elif qa == "DESCARGA ZIP ASESOR":
                    df_show = df_show[df_show["action"].astype(str) == "DESCARGA ZIP ASESOR"]
                elif qa == "DESCARGA DOCUMENTO":
                    df_show = df_show[df_show["action"].astype(str) == "DESCARGA DOCUMENTO"]
                else:
                    # OTROS: no filtrar por action; mostrar todo lo que no cae en las categorías anteriores
                    pass

            st.dataframe(df_show.reset_index(drop=True), use_container_width=True, hide_index=True)

            try:
                csv_bytes = df_show.to_csv(index=False, encoding="utf-8")
                st.download_button("⬇️ Descargar historial filtrado (CSV)", data=csv_bytes, file_name="historial_filtrado.csv", mime="text/csv")
            except Exception:
                pass
            if st.button("🗑️ Borrar historial"):
                try:
                    # Crear un CSV vacío con las columnas correctas
                    cols = ["id","nombre","estatus_old","estatus_new","segundo_old","segundo_new","observaciones","action","actor","ts"]
                    pd.DataFrame(columns=cols).to_csv(HISTORIAL_CSV, index=False, encoding="utf-8")
                    st.success("Historial eliminado correctamente.")
                    do_rerun()
                except Exception as e:
                    st.error(f"Error al borrar historial: {e}")