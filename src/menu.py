# menu.py
# Módulo 6 — Refactor: sin lógica de negocio en el menú,
# toda validación delegada a service/validate.

from colorama import init, Fore, Style

from service import (
    new_register,
    list_records,
    search_record,
    update_record,
    delete_record,
    usuarios,
)
from integration import generar_registros_falsos, previsualizar_registro
from validate import validar_cantidad

init(autoreset=True)

# ─── Helpers de presentación ─────────────────────────────────────────────────

def _ok(mensaje: str) -> None:
    """Imprime mensaje de éxito en verde."""
    print(Fore.GREEN + f"\n✔ {mensaje}")


def _error(mensaje: str) -> None:
    """Imprime mensaje de error en rojo."""
    print(Fore.RED + f"\n✘ Error: {mensaje}")


def _info(mensaje: str) -> None:
    """Imprime mensaje informativo en cian."""
    print(Fore.CYAN + f"\n── {mensaje} ──" + Style.RESET_ALL)


# ─── Menú ────────────────────────────────────────────────────────────────────

def mostrar_menu() -> None:
    """Imprime el menú principal con colores."""
    print(Style.BRIGHT + Fore.CYAN + "\n" + "=" * 40)
    print("       SISTEMA DE GESTIÓN DE USUARIOS")
    print("=" * 40 + Style.RESET_ALL)
    print("  1. Crear usuario")
    print("  2. Listar usuarios")
    print("  3. Buscar usuario")
    print("  4. Actualizar usuario")
    print("  5. Eliminar usuario")
    print(Fore.MAGENTA + "  6. Generar registros falsos (faker)" + Style.RESET_ALL)
    print("  0. Salir")
    print(Fore.CYAN + "=" * 40 + Style.RESET_ALL)


# ─── Acciones del menú ───────────────────────────────────────────────────────

def solicitar_usuario() -> None:
    """Recoge datos del usuario por teclado y delega la creación a service."""
    _info("Nuevo usuario")
    id_input     = input("ID: ").strip()
    nombre_input = input("Nombre: ").strip()
    correo_input = input("Correo: ").strip()
    edad_input   = input("Edad: ").strip()
    estado_input = input("Estado (Activo/Inactivo): ").strip()

    exito, mensaje = new_register(id_input, nombre_input, correo_input, edad_input, estado_input)
    _ok(mensaje) if exito else _error(mensaje)


def mostrar_usuarios() -> None:
    """Lista todos los usuarios ordenados por el campo que elija el usuario."""
    _info("Usuarios registrados")
    print("Ordenar por: id | nombre | correo | edad | estado")
    campo = input("Campo (Enter = id): ").strip().lower() or "id"

    ok, resultado = list_records(ordenar_por=campo)

    if not ok:
        _error(resultado)
    elif not resultado:
        print(Fore.YELLOW + "No hay usuarios registrados aún.")
    else:
        for linea in resultado:
            print(" •", linea)


def buscar_usuario() -> None:
    """Busca usuarios por ID exacto o texto parcial en nombre/correo."""
    _info("Buscar usuario")
    termino = input("ID o Nombre (parcial): ").strip()

    ok, resultado = search_record(termino)

    if not ok:
        _error(resultado)
    else:
        print(Fore.GREEN + f"\n{len(resultado)} resultado(s) encontrado(s):")
        for linea in resultado:
            print(" •", linea)


def actualizar_usuario() -> None:
    """Recoge campos opcionales y delega la actualización a service."""
    _info("Actualizar usuario")
    print("(Deja en blanco los campos que NO quieras cambiar)")
    id_input     = input("ID del usuario a actualizar: ").strip()
    nombre_input = input("Nuevo nombre: ").strip() or None
    correo_input = input("Nuevo correo: ").strip() or None
    edad_input   = input("Nueva edad: ").strip() or None
    estado_input = input("Nuevo estado (Activo/Inactivo): ").strip() or None

    exito, mensaje = update_record(id_input, nombre_input, correo_input, edad_input, estado_input)
    _ok(mensaje) if exito else _error(mensaje)


def eliminar_usuario() -> None:
    """Pide confirmación al usuario y delega la eliminación a service."""
    _info("Eliminar usuario")
    id_input = input("ID del usuario a eliminar: ").strip()

    confirmacion = input(
        f"¿Confirmas eliminar el usuario con ID {id_input}? (s/n): "
    ).strip().lower()

    if confirmacion != "s":
        print(Fore.YELLOW + "Operación cancelada.")
        return

    exito, mensaje = delete_record(id_input)
    _ok(mensaje) if exito else _error(mensaje)


def generar_falsos() -> None:
    """
    Muestra una vista previa, recoge la cantidad y estado opcional,
    y delega la generación a integration.generar_registros_falsos().

    La validación de cantidad ya no ocurre aquí — se delega a
    validate.validar_cantidad() a través de integration.py.
    """
    _info("Generar registros falsos")

    ejemplo = previsualizar_registro()
    print(Fore.CYAN + "\nEjemplo del registro que se generará:" + Style.RESET_ALL)
    for clave, valor in ejemplo.items():
        print(f"  {clave}: {valor}")

    print()
    cantidad_raw = input("¿Cuántos registros generar? (Enter = 10): ").strip()
    cantidad = cantidad_raw if cantidad_raw else "10"

    estado_input = input(
        "¿Forzar estado? (Activo / Inactivo / Enter = aleatorio): "
    ).strip().capitalize()

    kwargs_extra = {}
    if estado_input in ("Activo", "Inactivo"):
        kwargs_extra["estado"] = estado_input

    exito, mensaje = generar_registros_falsos(cantidad, **kwargs_extra)

    if exito:
        _ok(mensaje)
        print(Fore.CYAN + f"  Total de usuarios ahora: {len(usuarios)}" + Style.RESET_ALL)
    else:
        _error(mensaje)


# ─── Bucle principal ─────────────────────────────────────────────────────────

_OPCIONES: dict[str, object] = {
    "1": solicitar_usuario,
    "2": mostrar_usuarios,
    "3": buscar_usuario,
    "4": actualizar_usuario,
    "5": eliminar_usuario,
    "6": generar_falsos,
}


def main_menu() -> None:
    """Bucle principal del menú de consola."""
    total = len(usuarios)
    if total:
        print(Fore.GREEN + f"Sistema listo — {total} usuario(s) cargado(s) desde archivo.")
    else:
        print(Fore.YELLOW + "Sistema listo — sin registros previos.")

    while True:
        mostrar_menu()
        try:
            opcion = input("Elige una opción: ").strip()
        except EOFError:
            # Ocurre en pipes o redirección de stdin — salir limpiamente
            print(Fore.YELLOW + "\n\nFin de entrada. ¡Hasta luego!")
            break
        except KeyboardInterrupt:
            # Ctrl+C en el menú principal — confirmar salida
            try:
                respuesta = input(Fore.YELLOW + "\n\n¿Deseas salir? (s/n): ").strip().lower()
            except (KeyboardInterrupt, EOFError):
                respuesta = "s"
            if respuesta == "s":
                print(Fore.GREEN + "\n¡Hasta luego!")
                break
            continue

        if opcion == "0":
            print(Fore.GREEN + "\n¡Hasta luego!")
            break

        accion = _OPCIONES.get(opcion)
        if accion:
            try:
                accion()
            except (KeyboardInterrupt, EOFError):
                print(Fore.YELLOW + "\n\nOperación cancelada. Volviendo al menú.")
        else:
            print(Fore.RED + "\n⚠ Opción no válida. Intenta de nuevo.")