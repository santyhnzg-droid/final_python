# validate.py 
import re

def validar_id(id_usuario, ids_existentes):
    try:
        id_usuario = int(id_usuario)
        if id_usuario <= 0:
            return False, "El ID debe ser un número entero positivo."
        if id_usuario in ids_existentes:    
            return False, f"El ID {id_usuario} ya existe. Usa uno diferente."
        return True, id_usuario
    except ValueError:
        return False, "El ID debe ser un número entero."

def validar_nombre(nombre):
    nombre = nombre.strip()
    if not nombre:
        return False, "El nombre no puede estar vacío."
    if not re.match(r'^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]+$', nombre):
        return False, "El nombre solo puede contener letras y espacios."
    return True, nombre

def validar_correo(correo):
    correo = correo.strip().lower()
    patron = r'^[\w\.-]+@[\w\.-]+\.\w{2,}$'
    if not re.match(patron, correo):
        return False, "El correo no tiene un formato válido. Ejemplo: usuario@correo.com"
    return True, correo

def validar_edad(edad):
    try:
        edad = int(edad)
        if edad < 1 or edad > 100:
            return False, "La edad debe estar entre 1 y 100 años."
        return True, edad
    except ValueError:
        return False, "La edad debe ser un número entero."

def validar_estado(estado):
    """Acepta 'Activo' o 'Inactivo' en cualquier combinación de mayúsculas/minúsculas."""
    estado_normalizado = estado.strip().capitalize()
    if estado_normalizado in ("Activo", "Inactivo"):
        return True, estado_normalizado
    else:
        return False, "El estado debe ser 'Activo' o 'Inactivo'"