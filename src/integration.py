# integration.py
# Módulo 6 — Refactor: type hints, docstrings, validación centralizada,
# sin duplicación, sin 'global'

from typing import Any

from faker import Faker
from validate import validar_cantidad
from service import usuarios, ids_registrados, _persist

# Instancia de Faker en español
fake = Faker("es_ES")


# ─── Función genérica con *args y **kwargs ───────────────────────────────────

def construir_registro(*args: str, **kwargs: Any) -> dict[str, Any]:
    """
    Construye un diccionario de registro de forma genérica usando Faker.

    No persiste ni modifica el estado global — es una función pura
    de construcción; el guardado lo delega generar_registros_falsos().

    Args:
        *args: Nombres de campos a incluir del perfil completo.
               Si está vacío, se incluyen todos los campos estándar.
               El campo 'id' siempre se conserva.
        **kwargs: Valores que sobreescriben o añaden campos al registro.

    Returns:
        Diccionario con los datos del registro generado.
    """
    nuevo_id = _siguiente_id_disponible()

    perfil: dict[str, Any] = {
        "id":     nuevo_id,
        "nombre": f"{fake.first_name()} {fake.last_name()}",
        "correo": fake.email(),
        "edad":   fake.random_int(min=18, max=70),
        "estado": fake.random_element(elements=("Activo", "Inactivo")),
    }

    if args:
        campos_pedidos = {"id"} | set(args)
        perfil = {k: v for k, v in perfil.items() if k in campos_pedidos}

    perfil.update(kwargs)
    return perfil


def generar_registros_falsos(n: Any = 10, **kwargs: Any) -> tuple[bool, str]:
    """
    Genera `n` registros falsos y los persiste en el archivo JSON.

    La validación de `n` se delega a validar_cantidad() en validate.py
    (antes estaba duplicada aquí y en menu.py).

    Args:
        n: Cantidad de registros a generar (por defecto 10).
        **kwargs: Campos fijos que tendrán todos los registros generados.

    Returns:
        (True, mensaje_ok) o (False, mensaje_error).
    """
    ok, resultado = validar_cantidad(n)
    if not ok:
        return False, resultado

    cantidad: int = resultado

    for _ in range(cantidad):
        registro = construir_registro(**kwargs)
        ids_registrados.add(registro["id"])
        usuarios.append(registro)

    _persist()
    return True, f"{cantidad} registros falsos generados y guardados correctamente."


def previsualizar_registro(**kwargs: Any) -> dict[str, Any]:
    """
    Genera y devuelve 1 registro de ejemplo sin guardarlo ni modificar estado.

    Útil para que el usuario vea el formato antes de generar en masa.

    Args:
        **kwargs: Campos fijos a aplicar al ejemplo.

    Returns:
        Diccionario con los datos del registro de ejemplo.
    """
    return construir_registro(**kwargs)


# ─── Helper privado ─────────────────────────────────────────────────────────

def _siguiente_id_disponible() -> int:
    """
    Calcula el próximo ID disponible que no colisione con los existentes.

    Returns:
        Entero positivo único no presente en ids_registrados.
    """
    siguiente = max(ids_registrados, default=0) + 1
    while siguiente in ids_registrados:
        siguiente += 1
    return siguiente