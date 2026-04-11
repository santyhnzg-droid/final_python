# service.py
# Módulo 6 — Refactor: type hints, docstrings, sin 'global', sin duplicación

from typing import Any, Optional

from validate import (
    validar_id,
    validar_nombre,
    validar_correo,
    validar_edad,
    validar_estado,
)
from file import load_data, save_data, DEFAULT_DATA_PATH

# ─── Tipos ───────────────────────────────────────────────────────────────────

Usuario = dict[str, Any]
ServiceResult = tuple[bool, Any]

# ─── Estado en memoria ───────────────────────────────────────────────────────
# Se hidrata al importar el módulo. integration.py accede a estos objetos
# directamente para añadir registros generados por Faker.

usuarios: list[Usuario] = load_data()
ids_registrados: set[int] = {u["id"] for u in usuarios}

# Ruta activa (cambiable en tests mediante service.DATA_PATH = ...)
DATA_PATH: str = DEFAULT_DATA_PATH


def _persist() -> None:
    """Persiste el estado actual de `usuarios` en `DATA_PATH`."""
    save_data(usuarios, DATA_PATH)


# ─── CREATE ──────────────────────────────────────────────────────────────────

def new_register(
    id: Any,
    nombre: str,
    correo: str,
    edad: Any,
    estado: str,
) -> ServiceResult:
    """
    Crea un nuevo usuario, lo añade en memoria y lo persiste en disco.

    Args:
        id: Identificador único (se acepta str para compatibilidad con input()).
        nombre: Nombre completo del usuario.
        correo: Correo electrónico.
        edad: Edad (se acepta str para compatibilidad con input()).
        estado: 'Activo' o 'Inactivo'.

    Returns:
        (True, mensaje_ok) o (False, mensaje_error).
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

    nuevo: Usuario = {
        "id": id_val,
        "nombre": nombre_val,
        "correo": correo_val,
        "edad": edad_val,
        "estado": estado_val,
    }

    usuarios.append(nuevo)
    ids_registrados.add(id_val)
    _persist()

    return True, f"Usuario '{nombre_val}' creado exitosamente."


# ─── READ — listar ───────────────────────────────────────────────────────────

_CAMPOS_ORDEN: frozenset[str] = frozenset({"id", "nombre", "correo", "edad", "estado"})


def list_records(ordenar_por: str = "id") -> ServiceResult:
    """
    Devuelve todos los usuarios ordenados por el campo indicado.

    Args:
        ordenar_por: Campo por el que ordenar. Valores válidos:
                     'id', 'nombre', 'correo', 'edad', 'estado'.

    Returns:
        (True, lista_de_líneas_formateadas) o (False, mensaje_error).
    """
    if ordenar_por not in _CAMPOS_ORDEN:
        return False, f"Campo de orden inválido. Usa uno de: {', '.join(sorted(_CAMPOS_ORDEN))}"

    ordenados = sorted(usuarios, key=lambda u: u[ordenar_por])
    resumen = [_formatear_usuario(u) for u in ordenados]
    return True, resumen


# ─── READ — buscar ───────────────────────────────────────────────────────────

def search_record(termino: str) -> ServiceResult:
    """
    Busca usuarios cuyo nombre, correo o ID coincidan con el término.

    La búsqueda por nombre y correo es parcial e insensible a mayúsculas.
    La búsqueda por ID es exacta.

    Args:
        termino: Texto a buscar.

    Returns:
        (True, lista_de_líneas_formateadas) o (False, mensaje_error).
    """
    termino = termino.strip().lower()
    if not termino:
        return False, "El término de búsqueda no puede estar vacío."

    encontrados = [
        u for u in usuarios
        if termino in u["nombre"].lower()
        or termino in u["correo"].lower()
        or termino == str(u["id"])
    ]

    if not encontrados:
        return False, f"No se encontraron usuarios con el término '{termino}'."

    return True, [_formatear_usuario(u) for u in encontrados]


# ─── UPDATE ──────────────────────────────────────────────────────────────────

def update_record(
    id: Any,
    nombre: Optional[str] = None,
    correo: Optional[str] = None,
    edad: Optional[Any] = None,
    estado: Optional[str] = None,
) -> ServiceResult:
    """
    Actualiza uno o más campos del usuario identificado por `id`.

    Solo se modifican los campos cuyo valor no sea None.

    Args:
        id: ID del usuario a modificar.
        nombre: Nuevo nombre (opcional).
        correo: Nuevo correo (opcional).
        edad: Nueva edad (opcional).
        estado: Nuevo estado (opcional).

    Returns:
        (True, mensaje_ok) o (False, mensaje_error).
    """
    try:
        id_int = int(id)
    except (ValueError, TypeError):
        return False, "El ID debe ser un número entero."

    if id_int not in ids_registrados:
        return False, f"No existe ningún usuario con ID {id_int}."

    usuario = next((u for u in usuarios if u["id"] == id_int), None)
    if usuario is None:
        return False, f"No se pudo encontrar el usuario con ID {id_int}."

    campos_actualizados: list[str] = []

    # Tabla de (valor_nuevo, validador, clave_en_dict)
    actualizaciones = [
        (nombre, validar_nombre, "nombre"),
        (correo, validar_correo, "correo"),
        (edad,   validar_edad,   "edad"),
        (estado, validar_estado, "estado"),
    ]

    for valor, validador, clave in actualizaciones:
        if valor is not None:
            ok, resultado = validador(valor)
            if not ok:
                return False, resultado
            usuario[clave] = resultado
            campos_actualizados.append(clave)

    if not campos_actualizados:
        return False, "No se proporcionó ningún campo para actualizar."

    _persist()
    return True, f"Usuario ID {id_int} actualizado: {', '.join(campos_actualizados)}."


# ─── DELETE ──────────────────────────────────────────────────────────────────

def delete_record(id: Any) -> ServiceResult:
    """
    Elimina el usuario con el ID indicado.

    Args:
        id: ID del usuario a eliminar.

    Returns:
        (True, mensaje_ok) o (False, mensaje_error).
    """
    try:
        id_int = int(id)
    except (ValueError, TypeError):
        return False, "El ID debe ser un número entero."

    if id_int not in ids_registrados:
        return False, f"No existe ningún usuario con ID {id_int}."

    nombre_eliminado = next(
        (u["nombre"] for u in usuarios if u["id"] == id_int), "desconocido"
    )

    # Modificación in-place para no romper las referencias externas (integration.py)
    usuarios[:] = [u for u in usuarios if u["id"] != id_int]
    ids_registrados.discard(id_int)
    _persist()

    return True, f"Usuario '{nombre_eliminado}' (ID {id_int}) eliminado exitosamente."


# ─── Helper interno ──────────────────────────────────────────────────────────

def _formatear_usuario(u: Usuario) -> str:
    """
    Devuelve una línea legible con los datos de un usuario.
    Centraliza el formato antes duplicado en list_records y search_record.
    """
    return (
        f"[{u['id']}] {u['nombre']} | {u['correo']} "
        f"| Edad: {u['edad']} | Estado: {u['estado']}"
    )


# ─── Alias de compatibilidad ────────────────────────────────────────────────

def crear_usuario(id: Any, nombre: str, correo: str, edad: Any, estado: str) -> ServiceResult:
    """Alias de new_register para compatibilidad con módulos anteriores."""
    return new_register(id, nombre, correo, edad, estado)


def listar_usuarios() -> list[str]:
    """Alias de list_records() para compatibilidad con módulos anteriores."""
    ok, resultado = list_records()
    return resultado if ok else []