from pathlib import Path
import shutil
from .config import DOCS_DIR
from .utils import safe_name
from typing import Iterable, List

def carpeta_docs_cliente(cid: str) -> Path:
    name_safe = safe_name(str(cid))
    folder = DOCS_DIR / name_safe
    folder.mkdir(parents=True, exist_ok=True)
    return folder

def listar_docs_cliente(cid: str) -> List[Path]:
    folder = carpeta_docs_cliente(cid)
    return sorted([p for p in folder.iterdir() if p.is_file()], key=lambda p: p.name)

def subir_docs(cid: str, files: Iterable, prefijo: str = "") -> List[str]:
    if not cid or not files:
        return []
    folder = carpeta_docs_cliente(cid)
    saved = []
    for f in files:
        name = getattr(f, "name", None) or getattr(f, "filename", "uploaded")
        target = safe_name(f"{prefijo}{name}")
        try:
            data = None
            if hasattr(f, 'getbuffer'):
                data = f.getbuffer()
            elif hasattr(f, 'read'):
                data = f.read()
            if isinstance(data, memoryview):
                data = data.tobytes()
            if isinstance(data, str):
                data = data.encode('utf-8')
            Path(folder / target).write_bytes(data)
            saved.append(target)
        except Exception:
            continue
    return saved
