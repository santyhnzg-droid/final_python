# 📘 Sistema de Gestión de Usuarios

Aplicación de consola en Python que permite crear, listar, buscar, actualizar y eliminar usuarios,  
con persistencia en archivo JSON. Incluye generación automática de registros falsos usando la librería Faker.

---

## 🗂️ Estructura del proyecto

```
gestion-info/
├── README.md
├── requirements.txt
├── .gitignore
├── data/
│   └── records.json              # datos persistidos (se genera automáticamente)
├── src/
│   ├── main.py                   # punto de entrada
│   ├── menu.py                   # interfaz de consola (UI)
│   ├── service.py                # lógica (CRUD)
│   ├── file.py                   # persistencia (leer/guardar)
│   ├── validate.py               # validaciones y helpers
│   └── integration.py            # generación con Faker
└── test/
    └── tests.py                  # pruebas unitarias (87 casos)
```

---

## ▶️ Instalación

**1. Clonar el repositorio:**

```bash
git clone <url-del-repositorio>
cd gestion-info
```

**2. Crear entorno virtual (recomendado):**

```bash
python -m venv .venv

# Linux / macOS
source .venv/bin/activate

# Windows (PowerShell)
.venv\Scripts\Activate.ps1
```

**3. Instalar dependencias:**

```bash
pip install -r requirements.txt
```

Las dependencias incluyen `faker` (generación de datos falsos) y `colorama` (colores en consola).

**4. Ejecutar la aplicación:**

```bash
python src/main.py
```

---

## 🚀 Funcionalidades

| Opción | Descripción |
|--------|-------------|
| 1 | **Crear usuario** — Registra un nuevo usuario con ID, nombre, correo, edad y estado |
| 2 | **Listar usuarios** — Muestra todos los usuarios ordenados por el campo que elijas |
| 3 | **Buscar usuario** — Búsqueda parcial por nombre, correo o ID exacto |
| 4 | **Actualizar usuario** — Modifica campos individuales de un usuario existente |
| 5 | **Eliminar usuario** — Borra un usuario por su ID (pide confirmación) |
| 6 | **Generar registros falsos (Faker)** — Crea N usuarios aleatorios con datos en español |
| 0 | **Salir** — Guarda los datos y cierra la aplicación |

---

## 🔧 Uso de `*args` y `**kwargs`

En `integration.py` se usan `*args` y `**kwargs` para construir funciones genéricas de generación de datos:

### `construir_registro(*args, **kwargs)`

Construye un diccionario de usuario. Los campos que no se proporcionen se generan automáticamente con Faker.

```python
# Registro completamente aleatorio
registro = construir_registro()

# Registro con estado fijo, el resto aleatorio
registro = construir_registro(estado="Activo")

# Solo algunos campos del perfil
registro = construir_registro("nombre", "correo")

# Campos con valores específicos
registro = construir_registro(nombre="Ana López", edad=30)
```

### `generar_registros_falsos(n, **kwargs)`

Genera y persiste `n` usuarios falsos en el sistema.

- `n`: cantidad de registros a generar (por defecto 10).
- `**kwargs`: campos fijos que se aplican a todos los registros generados.

```python
# 10 registros completamente aleatorios
generar_registros_falsos()

# 5 registros, todos con estado "Activo"
generar_registros_falsos(5, estado="Activo")
```

---

## 🧪 Pruebas unitarias

**Ejecutar todas las pruebas:**

```bash
python test/tests.py
```

**Con detalle por prueba:**

```bash
python test/tests.py -v
```

Resultado esperado:

```
Ran 87 tests in ~0.07s

OK
```

Las pruebas cubren los módulos `validate`, `file`, `service` e `integration`.  
Usan archivos JSON temporales y limpian el estado en memoria entre cada test,  
sin modificar `data/records.json`.

---

## 🔒 Validaciones

Todas las validaciones están centralizadas en `validate.py` sin duplicación:

| Campo | Reglas |
|-------|--------|
| ID | Entero positivo, no duplicado |
| Nombre | Solo letras y espacios, no vacío |
| Correo | Formato `usuario@dominio.tld`, sin punto inicial |
| Edad | Entero entre 1 y 100 |
| Estado | Solo `Activo` o `Inactivo` |
| Cantidad | Entero mayor a 0 |

---

## 👤 Autor

**Santiago Hernández Galeano**  
Proyecto desarrollado como taller académico del curso de Python.

---

## 📄 Licencia

Uso educativo. Sin restricciones para fines de aprendizaje.