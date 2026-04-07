# service.py
# Módulo de lógica de negocio — ahora con persistencia en archivo

from validate import (
    validar_id,
    validar_nombre,
    validar_correo,
    validar_edad,
    validar_estado,
)
from file import load_data, save_data

# ─── Estructuras de datos (se inicializan desde archivo) ────────────────────

usuarios = load_data()
ids_registrados = {u["id"] for u in usuarios}  # Reconstruye el set desde el archivo


# ─── Funciones de servicio ───────────────────────────────────────────────────

def crear_usuario(id, nombre, correo, edad, estado):
    """
    Valida, guarda en memoria y persiste en archivo.
    Retorna (True, mensaje) o (False, mensaje_de_error).
    """
    ok, id_val = validar_id(id, ids_registrados)
    if not ok:
        return False, id_val

    ok, nombre_val = validar_nombre(nombre)
    if not ok:
        return False, nombre_val

    ok, correo_val = validar_correo(correo)
    if not ok:
        return False, correo_val

    ok, edad_val = validar_edad(edad)
    if not ok:
        return False, edad_val

    ok, estado_val = validar_estado(estado)
    if not ok:
        return False, estado_val

    nuevo_usuario = {
        "id": id_val,
        "nombre": nombre_val,
        "correo": correo_val,
        "edad": edad_val,
        "estado": estado_val,
    }

    usuarios.append(nuevo_usuario)
    ids_registrados.add(id_val)
    save_data(usuarios)  # ← persiste inmediatamente tras cada creación

    return True, f"Usuario '{nombre_val}' creado exitosamente."


def listar_usuarios():
    """
    Retorna una lista de strings con el resumen de cada usuario.
    """
    if not usuarios:
        return []

    return [
        f"[{u['id']}] {u['nombre']} | {u['correo']} | Edad: {u['edad']} | Estado: {u['estado']}"
        for u in usuarios
    ]
