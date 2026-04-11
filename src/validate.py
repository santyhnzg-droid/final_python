# validate.py
# Módulo 6 — Refactor: type hints, docstrings, constantes centralizadas

import re
from typing import Any

# ─── Constantes ─────────────────────────────────────────────────────────────

ESTADOS_VALIDOS: frozenset[str] = frozenset({"Activo", "Inactivo"})
PATRON_CORREO: re.Pattern[str] = re.compile(r'^[a-zA-Z0-9][\w\.-]*@[\w\.-]+\.\w{2,}$')
PATRON_NOMBRE: re.Pattern[str] = re.compile(r'^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]+$')
EDAD_MIN: int = 1
EDAD_MAX: int = 100

ValidationResult = tuple[bool, Any]


def validar_id(id_usuario: Any, ids_existentes: set[int]) -> ValidationResult:
    """
    Valida que el ID sea un entero positivo y no esté duplicado.

    Args:
        id_usuario: Valor a validar (puede llegar como str desde input()).
        ids_existentes: Conjunto de IDs ya registrados en memoria.

    Returns:
        (True, id_int) si es válido, (False, mensaje_error) si no.
    """
    try:
        id_int = int(id_usuario)
    except (ValueError, TypeError):
        return False, "El ID debe ser un número entero."
    if id_int <= 0:
        return False, "El ID debe ser un número entero positivo."
    if id_int in ids_existentes:
        return False, f"El ID {id_int} ya existe. Usa uno diferente."
    return True, id_int


def validar_nombre(nombre: str) -> ValidationResult:
    """
    Valida que el nombre no esté vacío y solo contenga letras y espacios.

    Args:
        nombre: Cadena con el nombre del usuario.

    Returns:
        (True, nombre_limpio) si es válido, (False, mensaje_error) si no.
    """
    nombre = nombre.strip()
    if not nombre:
        return False, "El nombre no puede estar vacío."
    if not PATRON_NOMBRE.match(nombre):
        return False, "El nombre solo puede contener letras y espacios."
    return True, nombre


def validar_correo(correo: str) -> ValidationResult:
    """
    Valida formato de correo electrónico (usuario@dominio.tld).

    Args:
        correo: Cadena con el correo a validar.

    Returns:
        (True, correo_normalizado) si es válido, (False, mensaje_error) si no.
    """
    correo = correo.strip().lower()
    if not PATRON_CORREO.match(correo):
        return False, "El correo no tiene un formato válido. Ejemplo: usuario@correo.com"
    return True, correo


def validar_edad(edad: Any) -> ValidationResult:
    """
    Valida que la edad sea un entero dentro del rango permitido.

    Args:
        edad: Valor a validar (puede llegar como str desde input()).

    Returns:
        (True, edad_int) si es válida, (False, mensaje_error) si no.
    """
    try:
        edad_int = int(edad)
    except (ValueError, TypeError):
        return False, "La edad debe ser un número entero."
    if not (EDAD_MIN <= edad_int <= EDAD_MAX):
        return False, f"La edad debe estar entre {EDAD_MIN} y {EDAD_MAX} años."
    return True, edad_int


def validar_estado(estado: str) -> ValidationResult:
    """
    Valida que el estado sea 'Activo' o 'Inactivo' (insensible a mayúsculas).

    Args:
        estado: Cadena con el estado a validar.

    Returns:
        (True, estado_normalizado) si es válido, (False, mensaje_error) si no.
    """
    estado_normalizado = estado.strip().capitalize()
    if estado_normalizado not in ESTADOS_VALIDOS:
        return False, "El estado debe ser 'Activo' o 'Inactivo'."
    return True, estado_normalizado


def validar_cantidad(cantidad: Any) -> ValidationResult:
    """
    Valida que una cantidad sea un entero positivo mayor a cero.
    Centraliza la validación antes duplicada en menu.py e integration.py.

    Args:
        cantidad: Valor a validar (puede llegar como str desde input()).

    Returns:
        (True, cantidad_int) si es válida, (False, mensaje_error) si no.
    """
    try:
        cantidad_int = int(cantidad)
    except (ValueError, TypeError):
        return False, "La cantidad debe ser un número entero."
    if cantidad_int < 1:
        return False, "La cantidad debe ser un número entero mayor a 0."
    return True, cantidad_int