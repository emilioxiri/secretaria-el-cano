import bcrypt
from models.usuario import Usuario

class UsuarioDAO:
    def __init__(self, db_manager):
        self.db_manager = db_manager

    def crear_usuario(self, nombre, email, plain_password):
        hashed_password = bcrypt.hashpw(plain_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        nuevo_usuario = Usuario(
            nombre=nombre,
            email=email,
            hashed_password=hashed_password,
            activo=True
        )
        with self.db_manager.get_db_session() as session:
            session.add(nuevo_usuario)
            session.commit()
        return nuevo_usuario

    def get_usuario_por_email(self, email):
        with self.db_manager.get_db_session() as session:
            return session.query(Usuario).filter_by(email=email).first()
