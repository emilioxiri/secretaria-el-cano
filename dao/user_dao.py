import bcrypt
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app import app
from models.usuario import Usuario

# Contraseña en texto plano
plain_password = "admin_password" # Elige una contraseña segura

# Hashear la contraseña
hashed_password_bytes = bcrypt.hashpw(plain_password.encode('utf-8'), bcrypt.gensalt())
hashed_password_str = hashed_password_bytes.decode('utf-8')

# Crear sesión de base de datos
Session = sessionmaker(bind=app.db_manager.engine)
session = Session()

# Crear el nuevo usuario
new_user = Usuario(
    nombre="Administrador",
    email="admin@falla.com",
    hashed_password=hashed_password_str
)

# Añadir y confirmar en la base de datos
try:
    session.add(new_user)
    session.commit()
    print("¡Usuario administrador creado con éxito!")
except Exception as e:
    print(f"Error al crear el usuario: {e}")
    session.rollback()
finally:
    session.close()