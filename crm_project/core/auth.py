"""Sistema de autenticación y gestión de usuarios"""
import streamlit as st
import hashlib
import secrets
import json
from pathlib import Path
from typing import Optional, Tuple
from crm_project.config.settings import USERS_FILE, PERMISSIONS


def _hash_pw_pbkdf2(password: str, salt_hex: Optional[str] = None) -> Tuple[str, str]:
    if not salt_hex:
        salt_hex = secrets.token_hex(16)
    salt = bytes.fromhex(salt_hex)
    dk = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, 100_000)
    return salt_hex, dk.hex()


def _verify_pw(password: str, salt_hex: str, hash_hex: str) -> bool:
    _, hh = _hash_pw_pbkdf2(password, salt_hex)
    return secrets.compare_digest(hh, hash_hex)


class UserManager:
    @staticmethod
    def load_users() -> dict:
        try:
            if USERS_FILE.exists():
                return json.loads(USERS_FILE.read_text(encoding="utf-8"))
        except Exception:
            pass
        return {"users": []}

    @staticmethod
    def save_users(data: dict):
        try:
            USERS_FILE.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
        except Exception as e:
            try:
                st.error(f"Error guardando usuarios: {e}")
            except Exception:
                pass

    @staticmethod
    def get_user(identifier: str) -> Optional[dict]:
        ident = (identifier or "").strip().lower()
        data = UserManager.load_users()
        for u in data.get("users", []):
            if u.get("user", "").lower() == ident:
                return u
        return None

    @staticmethod
    def add_user(username: str, password: str, role: str = "member") -> Tuple[bool, str]:
        uname = username.strip()
        if not uname or not password:
            return False, "Usuario y contraseña son obligatorios"
        if role not in ("admin", "member"):
            return False, "Rol inválido"
        data = UserManager.load_users()
        if any(u.get("user", "").lower() == uname.lower() for u in data.get("users", [])):
            return False, "Ese usuario ya existe"
        salt_hex, hash_hex = _hash_pw_pbkdf2(password)
        data["users"].append({"user": uname, "role": role, "salt": salt_hex, "hash": hash_hex})
        UserManager.save_users(data)
        return True, "Usuario creado"

    @staticmethod
    def delete_user(username: str) -> Tuple[bool, str]:
        name = username.strip().lower()
        if not name:
            return False, "Usuario inválido"
        data = UserManager.load_users()
        users = data.get("users", [])
        for i, u in enumerate(users):
            if u.get("user", "").lower() == name:
                users.pop(i)
                data["users"] = users
                UserManager.save_users(data)
                return True, "Usuario eliminado"
        return False, "Usuario no encontrado"


class AuthSession:
    @staticmethod
    def current_user() -> Optional[dict]:
        return st.session_state.get("auth_user")

    @staticmethod
    def is_authenticated() -> bool:
        return AuthSession.current_user() is not None

    @staticmethod
    def is_admin() -> bool:
        u = AuthSession.current_user()
        return bool(u and u.get("role") == "admin")

    @staticmethod
    def can(action: str) -> bool:
        u = AuthSession.current_user()
        role = (u or {}).get("role", "member")
        return PERMISSIONS.get(role, {}).get(action, False)

    @staticmethod
    def login(username: str, password: str) -> bool:
        user = UserManager.get_user(username)
        if user and _verify_pw(password, user.get("salt", ""), user.get("hash", "")):
            st.session_state["auth_user"] = {"user": user.get("user"), "role": user["role"]}
            return True
        return False

    @staticmethod
    def logout():
        st.session_state["auth_user"] = None
        for key in list(st.session_state.keys()):
            if key.startswith("f_") or key.startswith("login_"):
                st.session_state.pop(key, None)
