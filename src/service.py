# service.py
# Módulo de lógica de negocio para la gestión de usuarios en memoria

from validate import (
    validar_id,
    validar_nombre,
    validar_correo,
    validar_edad,
    validar_estado,
)

# ─── Estructuras de datos en memoria ────────────────────────────────────────

usuarios = []            # Lista de diccionarios: cada elemento es un usuario
ids_registrados = set()  # Set para garantizar IDs únicos


# ─── Funciones de servicio ───────────────────────────────────────────────────

def crear_usuario(id, nombre, correo, edad, estado):
    """
    Recibe los campos del usuario, los valida y los guarda en memoria.
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

    # Construir el diccionario del usuario
    nuevo_usuario = {
        "id": id_val,
        "nombre": nombre_val,
        "correo": correo_val,
        "edad": edad_val,
        "estado": estado_val,
    }

    # Guardar en la lista y registrar el ID en el set
    usuarios.append(nuevo_usuario)
    ids_registrados.add(id_val)

    return True, f"Usuario '{nombre_val}' creado exitosamente."


def listar_usuarios():
    """
    Retorna una lista de strings con el resumen de cada usuario.
    """
    if not usuarios:
        return []

    resumen = []
    for u in usuarios:
        linea = f"[{u['id']}] {u['nombre']} | {u['correo']} | Edad: {u['edad']} | Estado: {u['estado']}"
        resumen.append(linea)

    return resumen