# Secretaría El Cano

Sistema de gestión para la organización de fallas desarrollado con Streamlit y SQLAlchemy.

## Características

- **Gestión de Falleros**: Registro, consulta y administración de miembros de la falla
- **Sistema de Usuarios**: Autenticación y control de acceso
- **Interfaz Web**: Interfaz moderna y responsive construida con Streamlit
- **Base de Datos**: Integración con MySQL usando SQLAlchemy
- **Configuración Flexible**: Sistema de configuración basado en variables de entorno

## Instalación

### Requisitos

- Python 3.9+
- MySQL 5.7+ o MariaDB 10.3+
- Poetry (recomendado) o pip

### Configuración del Entorno

1. Clona el repositorio:
```bash
git clone https://github.com/emilioxiri/secretaria-el-cano.git
cd secretaria-el-cano
```

2. Instala las dependencias:
```bash
# Con Poetry (recomendado)
poetry install

# Con pip
pip install -r requirements.txt
```

3. Configura las variables de entorno:
```bash
cp .env.example .env
# Edita el archivo .env con tu configuración
```

4. Configura la base de datos:
```bash
# Ejecuta el script para crear el contenedor MySQL (opcional)
./run_mysql_container.sh

# O configura tu propia instancia MySQL y actualiza las variables de entorno
```

## Configuración

El sistema utiliza variables de entorno para la configuración. Copia el archivo `.env.example` a `.env` y modifica los valores según tu entorno:

### Variables de Base de Datos
- `DB_HOST`: Host de la base de datos (default: localhost)
- `DB_PORT`: Puerto de la base de datos (default: 3306)
- `DB_NAME`: Nombre de la base de datos (default: secretaria-el-cano)
- `DB_USERNAME`: Usuario de la base de datos
- `DB_PASSWORD`: Contraseña de la base de datos
- `DATABASE_URL`: URL completa de conexión (opcional)
- `INIT_DB`: Crear tablas al iniciar (true/false)

### Variables de Autenticación
- `AUTH_COOKIE_NAME`: Nombre de la cookie de sesión
- `AUTH_SECRET_KEY`: Clave secreta para la autenticación
- `AUTH_COOKIE_EXPIRY_DAYS`: Días de expiración de la cookie

### Variables de Aplicación
- `APP_NAME`: Nombre de la aplicación
- `APP_ICON`: Icono de la aplicación
- `APP_LAYOUT`: Layout de Streamlit (wide/centered)
- `LOGO_PATH`: Ruta al logo de la aplicación
- `DEBUG`: Modo debug (true/false)

## Uso

1. Inicia la aplicación:
```bash
# Con Poetry
poetry run streamlit run app.py

# Con Python directo
streamlit run app.py
```

2. Abre tu navegador en `http://localhost:8501`

3. Inicia sesión con un usuario válido

## Estructura del Proyecto

```
secretaria-el-cano/
├── app.py                 # Aplicación principal
├── config/
│   └── settings.py        # Configuración centralizada
├── constants/
│   └── messages.py        # Mensajes estáticos en español
├── dao/                   # Data Access Objects
│   ├── database.py        # Gestor de base de datos
│   ├── fallero_dao.py     # DAO para falleros
│   └── usuario_dao.py     # DAO para usuarios
├── managers/              # Lógica de negocio
│   ├── auth_manager.py    # Gestión de autenticación
│   ├── fallero_manager.py # Gestión de falleros
│   └── ui_manager.py      # Gestión de interfaz
├── models/                # Modelos de datos
│   ├── fallero.py         # Modelo Fallero
│   └── usuario.py         # Modelo Usuario
├── assets/                # Recursos estáticos
└── tests/                 # Tests unitarios
```

## Desarrollo

### Arquitectura

El proyecto sigue una arquitectura en capas:

- **Presentación** (`managers/ui_manager.py`): Interfaz de usuario con Streamlit
- **Lógica de Negocio** (`managers/`): Gestión de operaciones y validaciones
- **Acceso a Datos** (`dao/`): Operaciones de base de datos
- **Modelos** (`models/`): Definición de entidades
- **Configuración** (`config/`): Configuración centralizada

### Buenas Prácticas

- **Documentación**: Todos los docstrings están en inglés
- **Mensajes de Usuario**: Centralizados en español en `constants/messages.py`
- **Variables de Entorno**: Normalizadas en inglés
- **Tipado**: Uso de type hints en Python
- **Validación**: Validación de inputs en la capa de presentación
- **Separación de Responsabilidades**: Cada clase tiene una responsabilidad específica

### Testing

```bash
# Ejecutar tests
poetry run pytest

# Con coverage
poetry run pytest --cov=.
```

## Contribución

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo `LICENSE` para más detalles.

## Contacto

Emilio Honrubia - emilio.honrubia@gmail.com

Enlace del Proyecto: [https://github.com/emilioxiri/secretaria-el-cano](https://github.com/emilioxiri/secretaria-el-cano)
