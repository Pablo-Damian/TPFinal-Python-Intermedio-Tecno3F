# PYTHON-INTERMEDIO-TRABAJO-INTEGRADOR-FINAL-TECNO3F

# CRUD (muy simple) de usuarios con Python y SQLite

## Funcionamiento del Código

Este programa está escrito en Python y utiliza las siguientes bibliotecas:

1. `tkinter`: Para crear la interfaz gráfica de usuario (GUI).
2. `sqlite3`: Para manejar la base de datos SQLite.
3. `re`: Para realizar validaciones con expresiones regulares.

El código está estructurado en una clase principal llamada `CRUDUsuario`, que contiene todos los métodos necesarios para el funcionamiento de la aplicación:

- `__init__`: Inicializa la aplicación, crea la conexión a la base de datos y configura la interfaz.
- `create_tables`: Crea las tablas necesarias en la base de datos si no existen.
- `create_widgets`: Crea y configura los elementos de la interfaz gráfica.
- `load_user`, `create_record`, `read_records`, `update_record`, `delete_record`: Implementan las operaciones CRUD.
- `validate_inputs`: Valida (de forma muy básica) los datos ingresados por el usuario.
- `clear_entries`: Limpia los campos de entrada.
- `on_entry_click`, `on_focusout`: Manejan el texto de ayuda en el campo ID.

## Funcionamiento del Programa

Esta aplicación permite realizar operaciones CRUD (Crear, Leer, Actualizar, Eliminar) básicas sobre registros de usuarios almacenados en una base de datos SQLite.

### Interfaz

La interfaz consta de cinco campos de entrada:
- ID (solo para cargar usuarios existentes)
- Nombre
- Apellido
- Edad
- E-mail

Y cinco botones para las operaciones:
- Cargar Usuario
- Mostrar Usuarios
- Cargar Nuevo Usuario
- Actualizar Usuario
- Eliminar Usuario

### Operaciones

1. **Cargar Usuario**: Permite cargar los datos de un usuario existente introduciendo su ID.

2. **Mostrar Usuarios**: Muestra una lista de todos los usuarios almacenados en la base de datos.

3. **Cargar Nuevo Usuario**: Crea un nuevo registro de usuario con los datos introducidos en los campos.

4. **Actualizar Usuario**: Actualiza los datos del usuario cargado actualmente.

5. **Eliminar Usuario**: Elimina el usuario cargado actualmente de la base de datos.

### Validaciones

El programa incluye las siguientes validaciones (básicas):

- Nombre y Apellido: Deben contener solo letras.
- Edad: Debe ser un número entero positivo.
- E-mail: Debe contener '@' y terminar en '.com'.

Estas validaciones se realizan antes de crear o actualizar un registro.

### Base de Datos

La aplicación utiliza una base de datos SQLite con tres tablas relacionadas:
- `tabla1`: Almacena ID, nombre y apellido.
- `tabla2`: Almacena edad y se relaciona con `tabla1`.
- `tabla3`: Almacena email y se relaciona con `tabla2`.

Esta estructura permite una organización eficiente de los datos y mantiene la integridad referencial.

## Uso inicial de la aplicación

- Para poder 'Cargar...' un usuario hay que ingresar su ID (que se puede ver junto con todos sus datos con el botón 'Mostrar Usuarios').
- Para 'Actualizar...' o 'Eliminar...' un usuario primero debe estar cargado ingresando su ID.
- Para 'Crear...' un nuevo usuario sólo hay que ingresar sus datos y pulsar el botón correspondiente (no importa el ID ya que se creará de forma automática).
