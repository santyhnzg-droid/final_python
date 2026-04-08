# menu.py
# Módulo 4 — Interfaz de usuario con colores (colorama)

from colorama import init, Fore, Style
from service import (
    new_register,
    list_records,
    search_record,
    update_record,
    delete_record,
    usuarios
)

# Inicializa colorama (autoreset=True para que los colores no se acumulen)
init(autoreset=True)


def mostrar_menu():
    """Muestra el menú principal con colores."""
    print(Style.BRIGHT + Fore.CYAN + "\n" + "=" * 40)
    print("       SISTEMA DE GESTIÓN DE USUARIOS")
    print("=" * 40 + Style.RESET_ALL)
    print("  1. Crear usuario")
    print("  2. Listar usuarios")
    print("  3. Buscar usuario")
    print("  4. Actualizar usuario")
    print("  5. Eliminar usuario")
    print("  0. Salir")
    print(Fore.CYAN + "=" * 40 + Style.RESET_ALL)


def solicitar_usuario():
    """Solicita los datos para crear un nuevo usuario."""
    print(Fore.CYAN + "\n── Nuevo usuario ──" + Style.RESET_ALL)
    id_input = input("ID: ").strip()
    nombre_input = input("Nombre: ").strip()
    correo_input = input("Correo: ").strip()
    edad_input = input("Edad: ").strip()
    estado_input = input("Estado (Activo/Inactivo): ").strip()

    exito, mensaje = new_register(id_input, nombre_input, correo_input, edad_input, estado_input)
    if exito:
        print(Fore.GREEN + f"\n✔ {mensaje}")
    else:
        print(Fore.RED + f"\n✘ Error: {mensaje}")


def mostrar_usuarios():
    """Lista todos los usuarios ordenados por un campo."""
    print(Fore.CYAN + "\n── Usuarios registrados ──" + Style.RESET_ALL)
    print("Ordenar por: id | nombre | correo | edad | estado")
    campo = input("Campo (Enter = id): ").strip().lower() or "id"

    ok, resultado = list_records(ordenar_por=campo)

    if not ok:
        print(Fore.RED + f"\n✘ {resultado}")
    elif not resultado:
        print(Fore.YELLOW + "No hay usuarios registrados aún.")
    else:
        for linea in resultado:
            print(" •", linea)


def buscar_usuario():
    """Busca usuarios por ID (exacto) o por texto parcial en nombre/correo."""
    print(Fore.CYAN + "\n── Buscar usuario ──" + Style.RESET_ALL)
    termino = input("ID o Nombre (parcial): ").strip()

    ok, resultado = search_record(termino)

    if not ok:
        print(Fore.RED + f"\n✘ {resultado}")
    else:
        print(Fore.GREEN + f"\n{len(resultado)} resultado(s) encontrado(s):")
        for linea in resultado:
            print(" •", linea)


def actualizar_usuario():
    """Actualiza los campos que el usuario indique (deja vacío para no cambiar)."""
    print(Fore.CYAN + "\n── Actualizar usuario ──" + Style.RESET_ALL)
    print("(Deja en blanco los campos que NO quieras cambiar)")
    id_input = input("ID del usuario a actualizar: ").strip()
    nombre_input = input("Nuevo nombre: ").strip() or None
    correo_input = input("Nuevo correo: ").strip() or None
    edad_input = input("Nueva edad: ").strip() or None
    estado_input = input("Nuevo estado (Activo/Inactivo): ").strip() or None

    exito, mensaje = update_record(id_input, nombre_input, correo_input, edad_input, estado_input)
    if exito:
        print(Fore.GREEN + f"\n✔ {mensaje}")
    else:
        print(Fore.RED + f"\n✘ Error: {mensaje}")


def eliminar_usuario():
    """Elimina un usuario previa confirmación."""
    print(Fore.CYAN + "\n── Eliminar usuario ──" + Style.RESET_ALL)
    id_input = input("ID del usuario a eliminar: ").strip()

    confirmacion = input(f"¿Confirmas eliminar el usuario con ID {id_input}? (s/n): ").strip().lower()
    if confirmacion != "s":
        print(Fore.YELLOW + "Operación cancelada.")
        return

    exito, mensaje = delete_record(id_input)
    if exito:
        print(Fore.GREEN + f"\n✔ {mensaje}")
    else:
        print(Fore.RED + f"\n✘ Error: {mensaje}")


def main_menu():
    """Bucle principal del menú."""
    total = len(usuarios)
    if total:
        print(Fore.GREEN + f"Sistema listo — {total} usuario(s) cargado(s) desde archivo.")
    else:
        print(Fore.YELLOW + "Sistema listo — sin registros previos.")

    while True:
        mostrar_menu()
        try:
            opcion = input("Elige una opción: ").strip()
        except KeyboardInterrupt:
            print(Fore.YELLOW + "\n\nPrograma interrumpido. ¡Hasta luego!")
            break

        if opcion == "1":
            solicitar_usuario()
        elif opcion == "2":
            mostrar_usuarios()
        elif opcion == "3":
            buscar_usuario()
        elif opcion == "4":
            actualizar_usuario()
        elif opcion == "5":
            eliminar_usuario()
        elif opcion == "0":
            print(Fore.GREEN + "\n¡Hasta luego!")
            break
        else:
            print(Fore.RED + "\n⚠ Opción no válida. Intenta de nuevo.")