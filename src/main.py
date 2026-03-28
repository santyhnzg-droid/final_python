# main.py
# Punto de entrada del programa — Módulo 1

from service import crear_usuario, listar_usuarios


def mostrar_menu():
    print("\n" + "=" * 40)
    print("       SISTEMA DE GESTIÓN DE USUARIOS")
    print("=" * 40)
    print("  1. Crear usuario")
    print("  2. Listar usuarios")
    print("  0. Salir")
    print("=" * 40)


def solicitar_usuario():
    """Pide los datos del nuevo usuario por consola y llama a crear_usuario."""
    print("\n── Nuevo usuario ──")
    id_input = input("ID: ").strip()
    nombre_input = input("Nombre: ").strip()
    correo_input = input("Correo: ").strip()
    edad_input = input("Edad: ").strip()
    estado_input = input("Estado: ").strip()

    exito, mensaje = crear_usuario(id_input, nombre_input, correo_input, edad_input, estado_input)

    if exito:
        print(f"\n✔ {mensaje}")
    else:
        print(f"\n✘ Error: {mensaje}")


def mostrar_usuarios():
    """Lista todos los usuarios registrados en memoria."""
    print("\n── Usuarios registrados ──")
    resumen = listar_usuarios()

    if not resumen:
        print("No hay usuarios registrados aún.")
    else:
        for linea in resumen:
            print(" •", linea)


def main():
    print("Sistema listo")

    while True:
        mostrar_menu()

        try:
            opcion = input("Elige una opción: ").strip()
        except KeyboardInterrupt:
            print("\n\nPrograma interrumpido. ¡Hasta luego!")
            break

        if opcion == "1":
            solicitar_usuario()
        elif opcion == "2":
            mostrar_usuarios()
        elif opcion == "0":
            print("\n¡Hasta luego!")
            break
        else:
            print("\n⚠ Opción no válida. Intenta de nuevo.")


if __name__ == "__main__":
    main()