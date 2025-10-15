import json
import secrets
import hashlib
from .config import USERS_FILE

def _hash_pw_pbkdf2(password: str, salt_hex: str | None = None) -> tuple[str, str]:
    if not salt_hex:
        salt_hex = secrets.token_hex(16)
    salt = bytes.fromhex(salt_hex)
    dk = hashlib.pbkdf2_hmac("sha256", (password or "").encode("utf-8"), salt, 100_000)
    return salt_hex, dk.hex()

def _verify_pw(password: str, salt_hex: str, hash_hex: str) -> bool:
    _, hh = _hash_pw_pbkdf2(password, salt_hex)
    return secrets.compare_digest(hh, (hash_hex or ""))

def load_users_local() -> dict:
    try:
        if USERS_FILE.exists():
            return json.loads(USERS_FILE.read_text(encoding="utf-8"))
    except Exception:
        pass
    return {"users": []}

def save_users_local(obj: dict):
    try:
        USERS_FILE.write_text(json.dumps(obj, indent=2, ensure_ascii=False), encoding="utf-8")
    except Exception:
        pass

def add_user_local(username: str, password: str, role: str = "member") -> tuple[bool, str]:
    uname = (username or "").strip()
    if not uname or not password:
        return False, "Usuario y contraseña obligatorios."
    if role not in ("admin", "member"):
        return False, "Rol inválido."
    data = load_users_local()
    lower_uname = uname.lower()
    if any((u.get("user","") or u.get("email","" )).lower() == lower_uname for u in data.get("users", [])):
        return False, "Ese usuario ya existe."
    salt_hex, hash_hex = _hash_pw_pbkdf2(password)
    data["users"].append({"user": uname, "role": role, "salt": salt_hex, "hash": hash_hex})
    save_users_local(data)
    return True, "Usuario creado."

def delete_user_local(username: str) -> tuple[bool, str]:
    name = (username or "").strip().lower()
    if not name:
        return False, "Usuario inválido."
    data = load_users_local()
    users = data.get("users", [])
    for i, u in enumerate(users):
        if (u.get("user","") or u.get("email","" )).lower() == name:
            users.pop(i)
            data["users"] = users
            save_users_local(data)
            return True, "Usuario eliminado."
    return False, "Usuario no encontrado."
