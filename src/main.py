# main.py
# Punto de entrada del programa.

from menu import main_menu

if __name__ == "__main__":
    try:
        main_menu()
    except (KeyboardInterrupt, EOFError):
        pass