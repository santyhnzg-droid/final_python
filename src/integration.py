# integration.py
# Módulo 5 — Funciones avanzadas + Librería externa (faker)
#
# Responsabilidad: generar registros falsos pero realistas usando faker,
# aplicando *args y **kwargs para crear una función genérica de construcción.

from faker import Faker
from service import usuarios, ids_registrados, save_data

# Instancia de Faker en español
fake = Faker("es_ES")


# ─── Función genérica con *args y **kwargs ───────────────────────────────────

def construir_registro(*args, **kwargs):
    """
    Construye un diccionario de registro de forma genérica.

    *args   → campos que se quieren incluir del perfil faker completo.
              Si está vacío, se incluyen todos los campos estándar.
              Ejemplo: construir_registro("nombre", "correo")

    **kwargs → valores que sobreescriben o añaden campos al registro generado.
               Ejemplo: construir_registro(estado="Inactivo")

    Retorna un dict listo para guardar.
    """
    # Genera un ID único que no colisione con los existentes
    nuevo_id = max(ids_registrados, default=0) + 1
    while nuevo_id in ids_registrados:
        nuevo_id += 1

    # Perfil base generado por faker
    perfil_completo = {
        "id":     nuevo_id,
        "nombre": fake.first_name() + " " + fake.last_name(),
        "correo": fake.email(),
        "edad":   fake.random_int(min=18, max=70),
        "estado": fake.random_element(elements=("Activo", "Inactivo")),
    }

    # Si se pasaron campos específicos en *args, filtra solo esos
    # (siempre se conserva "id" porque es obligatorio)
    if args:
        campos_pedidos = {"id"} | set(args)
        perfil_completo = {
            k: v for k, v in perfil_completo.items()
            if k in campos_pedidos
        }

    # **kwargs sobreescribe o añade campos al resultado final
    perfil_completo.update(kwargs)

    return perfil_completo


# ─── Función principal: generar N registros y guardarlos ────────────────────

def generar_registros_falsos(n=10, **kwargs):
    """
    Genera n registros falsos y los persiste en el archivo JSON.

    n       → cantidad de registros a generar (por defecto 10).
    **kwargs → campos fijos que tendrán TODOS los registros generados.
               Ejemplo: generar_registros_falsos(5, estado="Activo")

    Retorna (True, mensaje) o (False, mensaje_error).
    """
    if not isinstance(n, int) or n < 1:
        return False, "La cantidad debe ser un número entero mayor a 0."

    generados = []

    for _ in range(n):
        registro = construir_registro(**kwargs)

        # Registra el ID en memoria para que el siguiente no colisione
        ids_registrados.add(registro["id"])
        usuarios.append(registro)
        generados.append(registro)

    save_data(usuarios)

    return True, f"{n} registros falsos generados y guardados correctamente."


# ─── Función de vista previa (sin guardar) ──────────────────────────────────

def previsualizar_registro(**kwargs):
    """
    Genera y muestra 1 registro de ejemplo sin guardarlo.
    Útil para que el usuario vea el formato antes de generar en masa.
    """
    ejemplo = construir_registro(**kwargs)
    # No lo agrega a usuarios ni guarda — solo muestra
    return ejemplo