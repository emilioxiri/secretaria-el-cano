"""
Static messages module for the Secretaria El Cano application.
All user-facing messages should be defined here in Spanish.
"""

class Messages:
    """Static messages in Spanish for user interface."""
    
    # Authentication messages
    AUTH_LOGIN_REQUIRED = "Por favor, inicia sesión."
    AUTH_LOGIN_FAILED = "Login fallido. Verifica tus credenciales."
    AUTH_NO_ACTIVE_USERS = "No hay usuarios activos en la base de datos. Contacta con el administrador."
    AUTH_LOGGED_IN_AS = "Conectado como"
    AUTH_LOGOUT = "Cerrar Sesión"
    AUTH_WELCOME = "Bienvenido"
    
    # Database messages
    DB_NOT_EXISTS = "La base de datos no existe. Define INIT_DB=True para crearla."
    DB_ERROR_INSERT_FALLERO = "Error al insertar el fallero: {error}"
    DB_ERROR_INSERT_USER = "Error al insertar el usuario: {error}"
    
    # Navigation and menu
    MENU_NAVIGATION = "Menú de Navegación"
    MENU_VIEW_FALLEROS = "Ver Falleros"
    MENU_ADD_FALLERO = "Añadir Fallero"
    MENU_VIEW_USERS = "Ver Usuarios"
    MENU_SELECT_OPTION = "Selecciona una opción del menú."
    
    # Falleros section
    FALLEROS_TITLE = "Listado de Falleros"
    FALLEROS_FILTER_TITLE = "🔎 Filtrar Falleros"
    FALLEROS_FILTER_NAME = "Filtrar por Nombre:"
    FALLEROS_FILTER_SURNAME = "Filtrar por Apellidos:"
    FALLEROS_FILTER_STATUS = "Filtrar por Estado:"
    FALLEROS_STATUS_ALL = "Todos"
    FALLEROS_STATUS_ACTIVE = "Activos"
    FALLEROS_STATUS_INACTIVE = "Inactivos"
    FALLEROS_NOT_FOUND = "No se encontraron falleros con los filtros seleccionados."
    FALLEROS_TOTAL_SHOWN = "Total de falleros mostrados: {count}"
    
    # Add fallero section
    ADD_FALLERO_TITLE = "Añadir Fallero/a"
    ADD_FALLERO_NAME = "Nombre*"
    ADD_FALLERO_SURNAME = "Apellidos*"
    ADD_FALLERO_DNI = "DNI*"
    ADD_FALLERO_DNI_HELP = "Formato: 8 números y una letra (ej: 12345678A)"
    ADD_FALLERO_BIRTH_DATE = "Fecha de nacimiento*"
    ADD_FALLERO_SUBMIT = "Añadir Fallero"
    ADD_FALLERO_SUCCESS = "Fallero añadido correctamente."
    
    # Users section
    USERS_TITLE = "Listado de Usuarios"
    USERS_FILTER_TITLE = "🔎 Filtrar Usuarios"
    USERS_FILTER_USERNAME = "Filtrar por Nombre de usuario:"
    USERS_FILTER_EMAIL = "Filtrar por Email:"
    USERS_FILTER_STATUS = "Filtrar por Estado:"
    USERS_NOT_FOUND = "No se encontraron usuarios con los filtros seleccionados."
    USERS_TOTAL_SHOWN = "Total de usuarios mostrados: {count}"
    USERS_ADD_BUTTON_HELP = "Añadir usuario"
    
    # Add user section
    ADD_USER_TITLE = "Añadir nuevo usuario"
    ADD_USER_USERNAME = "Nombre de usuario*"
    ADD_USER_EMAIL = "Email*"
    ADD_USER_PASSWORD = "Contraseña*"
    ADD_USER_ACTIVE = "Activo"
    ADD_USER_SUBMIT = "Crear usuario"
    ADD_USER_CANCEL = "Cancelar"
    ADD_USER_SUCCESS = "Usuario añadido correctamente."
    
    # Validation messages
    VALIDATION_NAME_REQUIRED = "El nombre es obligatorio."
    VALIDATION_SURNAME_REQUIRED = "Los apellidos son obligatorios."
    VALIDATION_DNI_INVALID = "El DNI debe tener 8 números y una letra (ej: 12345678A)."
    VALIDATION_USERNAME_REQUIRED = "El nombre de usuario es obligatorio."
    VALIDATION_EMAIL_INVALID = "El email debe tener un formato válido."
    VALIDATION_PASSWORD_MIN_LENGTH = "La contraseña debe tener al menos 6 caracteres."

class AuthTranslations:
    """Translation mappings for streamlit-authenticator component."""
    
    LOGIN_FORM = {
        'Form name': 'Secretaria El Cano',
        'Username': 'Usuario',
        'Password': 'Contraseña',
        'Login': 'Entrar',
        'Logged in as': 'Conectado como',
        'Incorrect username or password': 'Usuario o contraseña incorrectos',
        'Please enter username and password': 'Por favor, introduce usuario y contraseña',
    }