# file.py
# Módulo 6 — Refactor: ruta configurable, type hints, docstrings

import json
import os
from typing import Any

# ─── Ruta por defecto (sobreescribible en tests) ────────────────────────────

DEFAULT_DATA_PATH: str = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "data",
    "registros.json",
)


def load_data(ruta: str = DEFAULT_DATA_PATH) -> list[dict[str, Any]]:
    """
    Carga los usuarios desde el archivo JSON indicado.

    - Si el archivo no existe, retorna lista vacía (arranque limpio).
    - Si el JSON está dañado o el formato es inesperado, retorna lista vacía
      y muestra un aviso al usuario.

    Args:
        ruta: Ruta absoluta o relativa al archivo JSON.

    Returns:
        Lista de diccionarios de usuarios, o [] ante cualquier error.
    """
    if not os.path.exists(ruta):
        return []

    try:
        with open(ruta, "r", encoding="utf-8") as f:
            datos = json.load(f)
    except (json.JSONDecodeError, UnicodeDecodeError): # <--- Agregamos UnicodeDecodeError
        print("⚠ El archivo de datos está dañado o corrupto. Se inicia con lista vacía.")
        return []
    except OSError as e:
        print(f"⚠ No se pudo leer el archivo: {e}. Se inicia con lista vacía.")
        return []

    if not isinstance(datos, list):
        print("⚠ El archivo de datos tiene un formato inesperado. Se inicia con lista vacía.")
        return []

    return datos


def save_data(data: list[dict[str, Any]], ruta: str = DEFAULT_DATA_PATH) -> None:
    """
    Guarda la lista de usuarios en el archivo JSON indicado.

    Crea el directorio padre si no existe. Muestra un aviso si falla
    la escritura (no relanza la excepción para no interrumpir el flujo
    del menú).

    Args:
        data: Lista de diccionarios de usuarios a persistir.
        ruta: Ruta absoluta o relativa al archivo JSON destino.
    """
    try:
        os.makedirs(os.path.dirname(ruta), exist_ok=True)
        with open(ruta, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    except OSError as e:
        print(f"✘ Error al guardar los datos: {e}")