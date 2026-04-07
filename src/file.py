# file.py
# Módulo 2 — Persistencia en archivos JSON

import json
import os

RUTA_ARCHIVO = "data/registros.json"


def load_data():
    """
    Carga los usuarios desde el archivo JSON.
    - Si el archivo no existe, retorna lista vacía (arranque limpio).
    - Si el archivo está dañado, muestra mensaje y retorna lista vacía.
    """
    if not os.path.exists(RUTA_ARCHIVO):
        return []

    try:
        with open(RUTA_ARCHIVO, "r", encoding="utf-8") as f:
            datos = json.load(f)
            if not isinstance(datos, list):
                print("⚠ El archivo de datos tiene un formato inesperado. Se inicia con lista vacía.")
                return []
            return datos
    except json.JSONDecodeError:
        print("⚠ El archivo de datos está dañado o corrupto. Se inicia con lista vacía.")
        return []
    except OSError as e:
        print(f"⚠ No se pudo leer el archivo: {e}. Se inicia con lista vacía.")
        return []


def save_data(data):
    """
    Guarda la lista de usuarios en el archivo JSON.
    - Crea el directorio 'data/' si no existe.
    - Muestra mensaje si ocurre un error de escritura.
    """
    try:
        os.makedirs(os.path.dirname(RUTA_ARCHIVO), exist_ok=True)
        with open(RUTA_ARCHIVO, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    except OSError as e:
        print(f"✘ Error al guardar los datos: {e}")
