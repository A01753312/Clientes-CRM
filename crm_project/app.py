"""Punto de entrada principal del CRM (modo modular)"""
import streamlit as st
from crm_project.config.settings import COLUMNS
from crm_project.core.auth import AuthSession, UserManager
from crm_project.core.database import ClienteDB
from crm_project.components.sidebar import render_sidebar
from crm_project.features import dashboard
from crm_project.utils.helpers import find_logo, do_rerun

st.set_page_config(page_title="CRM Kapitaliza", page_icon="💼", layout="wide")

if "auth_user" not in st.session_state:
    st.session_state["auth_user"] = None

users_data = UserManager.load_users()
if not users_data.get("users"):
    with st.sidebar.expander("Configurar administrador", expanded=True):
        st.warning("No hay usuarios. Crea el primer administrador.")
        with st.form("setup_admin"):
            _user = st.text_input("Usuario admin")
            _pw1 = st.text_input("Contraseña", type="password")
            _pw2 = st.text_input("Confirmar", type="password")
            if st.form_submit_button("Crear administrador"):
                if not _user or not _pw1:
                    st.error("Usuario y contraseña obligatorios")
                elif _pw1 != _pw2:
                    st.error("Las contraseñas no coinciden")
                else:
                    ok, msg = UserManager.add_user(_user, _pw1, role="admin")
                    if ok:
                        st.success("Administrador creado. Inicia sesión.")
                        st.experimental_rerun()
                    else:
                        st.error(msg)
    st.stop()

if not AuthSession.is_authenticated():
    with st.sidebar.form("login_form"):
        st.markdown("### Iniciar sesión")
        luser = st.text_input("Usuario")
        lpw = st.text_input("Contraseña", type="password")
        submitted = st.form_submit_button("Entrar")
        if submitted:
            if AuthSession.login(luser, lpw):
                st.success("Bienvenido!")
                st.experimental_rerun()
            else:
                st.error("Credenciales inválidas")
    st.stop()

# Sidebar
df_filtrado = render_sidebar()

# Header
logo = find_logo()
if logo:
    col1, col2 = st.columns([1, 4])
    with col1:
        st.image(str(logo), width=200)
    with col2:
        st.title("💼 CRM Kapitaliza")
else:
    st.title("💼 CRM Kapitaliza")

# Tabs
tabs = st.tabs([
    "📊 Dashboard",
    "📋 Clientes",
    "📎 Documentos",
    "📥 Importar",
    "🗂️ Historial",
    "👥 Asesores"
])

with tabs[0]:
    dashboard.render(df_filtrado)

with tabs[1]:
    st.info("Pestaña Clientes pendiente de migración")

with tabs[2]:
    st.info("Pestaña Documentos pendiente de migración")

with tabs[3]:
    st.info("Pestaña Importar pendiente de migración")

with tabs[4]:
    st.info("Pestaña Historial pendiente de migración")

with tabs[5]:
    st.info("Pestaña Asesores pendiente de migración")
