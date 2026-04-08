# main.py
# Punto de entrada del programa — Módulo 3 (CRUD completo)

from service import (
    new_register,
    list_records,
    search_record,
    update_record,
    delete_record,
    usuarios,
)


def mostrar_menu():
    print("\n" + "=" * 40)
    print("       SISTEMA DE GESTIÓN DE USUARIOS")
    print("=" * 40)
    print("  1. Crear usuario")
    print("  2. Listar usuarios")
    print("  3. Buscar usuario")
    print("  4. Actualizar usuario")
    print("  5. Eliminar usuario")
    print("  0. Salir")
    print("=" * 40)


# ─── Opción 1: Crear ────────────────────────────────────────────────────────

def solicitar_usuario():
    print("\n── Nuevo usuario ──")
    id_input     = input("ID: ").strip()
    nombre_input = input("Nombre: ").strip()
    correo_input = input("Correo: ").strip()
    edad_input   = input("Edad: ").strip()
    estado_input = input("Estado (Activo): ").strip()

    exito, mensaje = new_register(id_input, nombre_input, correo_input, edad_input, estado_input)
    print(f"\n✔ {mensaje}" if exito else f"\n✘ Error: {mensaje}")


# ─── Opción 2: Listar ────────────────────────────────────────────────────────

def mostrar_usuarios():
    print("\n── Usuarios registrados ──")
    print("Ordenar por: id | nombre | correo | edad | estado")
    campo = input("Campo (Enter = id): ").strip() or "id"

    ok, resultado = list_records(ordenar_por=campo)

    if not ok:
        print(f"\n✘ {resultado}")
    elif not resultado:
        print("No hay usuarios registrados aún.")
    else:
        for linea in resultado:
            print(" •", linea)


# ─── Opción 3: Buscar ────────────────────────────────────────────────────────

def buscar_usuario():
    print("\n── Buscar usuario ──")
    termino = input("Nombre o correo (parcial): ").strip()

    ok, resultado = search_record(termino)

    if not ok:
        print(f"\n✘ {resultado}")
    else:
        print(f"\n{len(resultado)} resultado(s) encontrado(s):")
        for linea in resultado:
            print(" •", linea)


# ─── Opción 4: Actualizar ────────────────────────────────────────────────────

def actualizar_usuario():
    print("\n── Actualizar usuario ──")
    print("(Deja en blanco los campos que NO quieras cambiar)")
    id_input     = input("ID del usuario a actualizar: ").strip()
    nombre_input = input("Nuevo nombre: ").strip() or None
    correo_input = input("Nuevo correo: ").strip() or None
    edad_input   = input("Nueva edad: ").strip() or None
    estado_input = input("Nuevo estado (Activo): ").strip() or None

    exito, mensaje = update_record(id_input, nombre_input, correo_input, edad_input, estado_input)
    print(f"\n✔ {mensaje}" if exito else f"\n✘ Error: {mensaje}")


# ─── Opción 5: Eliminar ──────────────────────────────────────────────────────

def eliminar_usuario():
    print("\n── Eliminar usuario ──")
    id_input = input("ID del usuario a eliminar: ").strip()

    confirmacion = input(f"¿Confirmas eliminar el usuario con ID {id_input}? (s/n): ").strip().lower()
    if confirmacion != "s":
        print("Operación cancelada.")
        return

    exito, mensaje = delete_record(id_input)
    print(f"\n✔ {mensaje}" if exito else f"\n✘ Error: {mensaje}")


# ─── Main ────────────────────────────────────────────────────────────────────

def main():
    total = len(usuarios)
    if total:
        print(f"Sistema listo — {total} usuario(s) cargado(s) desde archivo.")
    else:
        print("Sistema listo — sin registros previos.")

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
        elif opcion == "3":
            buscar_usuario()
        elif opcion == "4":
            actualizar_usuario()
        elif opcion == "5":
            eliminar_usuario()
        elif opcion == "0":
            print("\n¡Hasta luego!")
            break
        else:
            print("\n⚠ Opción no válida. Intenta de nuevo.")


if __name__ == "__main__":
    main()
