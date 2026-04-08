# service.py
# Módulo 3 — CRUD completo con persistencia

from validate import (
    validar_id,
    validar_nombre,
    validar_correo,
    validar_edad,
    validar_estado,
)
from file import load_data, save_data

# ─── Datos en memoria (hidratados desde archivo al importar) ────────────────

usuarios = load_data()
ids_registrados = {u["id"] for u in usuarios}


# ─── CREATE ─────────────────────────────────────────────────────────────────

def new_register(id, nombre, correo, edad, estado):
    """
    Crea un nuevo usuario, lo guarda en memoria y persiste en archivo.
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

    nuevo = {
        "id": id_val,
        "nombre": nombre_val,
        "correo": correo_val,
        "edad": edad_val,
        "estado": estado_val,
    }

    usuarios.append(nuevo)
    ids_registrados.add(id_val)
    save_data(usuarios)

    return True, f"Usuario '{nombre_val}' creado exitosamente."


# ─── READ — listar ───────────────────────────────────────────────────────────

def list_records(ordenar_por="id"):
    """
    Retorna todos los usuarios ordenados por el campo indicado.
    Usa lambda para el criterio de orden.
    Campos válidos: 'id', 'nombre', 'correo', 'edad', 'estado'.
    """
    campos_validos = {"id", "nombre", "correo", "edad", "estado"}

    if ordenar_por not in campos_validos:
        return False, f"Campo de orden inválido. Usa uno de: {', '.join(campos_validos)}"

    ordenados = sorted(usuarios, key=lambda u: u[ordenar_por])

    # List comprehension para formatear cada línea
    resumen = [
        f"[{u['id']}] {u['nombre']} | {u['correo']} | Edad: {u['edad']} | Estado: {u['estado']}"
        for u in ordenados
    ]

    return True, resumen


# ─── READ — buscar ───────────────────────────────────────────────────────────

def search_record(termino):
    """
    Busca usuarios cuyo nombre o correo contengan el término (sin distinción de mayúsculas).
    Usa list comprehension para el filtrado.
    Retorna (True, lista_de_resultados) o (False, mensaje).
    """
    termino = termino.strip().lower()

    if not termino:
        return False, "El término de búsqueda no puede estar vacío."

    # List comprehension con condición múltiple
    encontrados = [
        u for u in usuarios
        if termino in u["nombre"].lower() or termino in u["correo"].lower()
    ]

    if not encontrados:
        return False, f"No se encontraron usuarios con el término '{termino}'."

    resumen = [
        f"[{u['id']}] {u['nombre']} | {u['correo']} | Edad: {u['edad']} | Estado: {u['estado']}"
        for u in encontrados
    ]

    return True, resumen


# ─── UPDATE ──────────────────────────────────────────────────────────────────

def update_record(id, nombre=None, correo=None, edad=None, estado=None):
    """
    Actualiza los campos indicados del usuario con el ID dado.
    Solo modifica los campos que se pasen (no None).
    Retorna (True, mensaje) o (False, mensaje_de_error).
    """
    try:
        id_int = int(id)
    except ValueError:
        return False, "El ID debe ser un número entero."

    if id_int not in ids_registrados:
        return False, f"No existe ningún usuario con ID {id_int}."

    # Buscar el usuario usando next + lambda (filter)
    usuario = next(filter(lambda u: u["id"] == id_int, usuarios), None)

    if usuario is None:
        return False, f"No se pudo encontrar el usuario con ID {id_int}."

    campos_actualizados = []

    if nombre is not None:
        ok, nombre_val = validar_nombre(nombre)
        if not ok:
            return False, nombre_val
        usuario["nombre"] = nombre_val
        campos_actualizados.append("nombre")

    if correo is not None:
        ok, correo_val = validar_correo(correo)
        if not ok:
            return False, correo_val
        usuario["correo"] = correo_val
        campos_actualizados.append("correo")

    if edad is not None:
        ok, edad_val = validar_edad(edad)
        if not ok:
            return False, edad_val
        usuario["edad"] = edad_val
        campos_actualizados.append("edad")

    if estado is not None:
        ok, estado_val = validar_estado(estado)
        if not ok:
            return False, estado_val
        usuario["estado"] = estado_val
        campos_actualizados.append("estado")

    if not campos_actualizados:
        return False, "No se proporcionó ningún campo para actualizar."

    save_data(usuarios)

    return True, f"Usuario ID {id_int} actualizado: {', '.join(campos_actualizados)}."


# ─── DELETE ──────────────────────────────────────────────────────────────────

def delete_record(id):
    """
    Elimina el usuario con el ID dado.
    Retorna (True, mensaje) o (False, mensaje_de_error).
    """
    try:
        id_int = int(id)
    except ValueError:
        return False, "El ID debe ser un número entero."

    if id_int not in ids_registrados:
        return False, f"No existe ningún usuario con ID {id_int}."

    global usuarios
    nombre_eliminado = next((u["nombre"] for u in usuarios if u["id"] == id_int), "desconocido")

    # List comprehension para reconstruir la lista sin el usuario eliminado
    usuarios = [u for u in usuarios if u["id"] != id_int]
    ids_registrados.discard(id_int)
    save_data(usuarios)

    return True, f"Usuario '{nombre_eliminado}' (ID {id_int}) eliminado exitosamente."


# ─── Alias de compatibilidad con Módulo 1 y 2 ───────────────────────────────

def crear_usuario(id, nombre, correo, edad, estado):
    return new_register(id, nombre, correo, edad, estado)


def listar_usuarios():
    ok, resultado = list_records()
    return resultado if ok else []
