from models.fallero import Fallero

class FalleroDAO:
    def __init__(self, db_manager):
        self.db_manager = db_manager

    def crear_fallero(self, nombre, apellidos, dni, fecha_nacimiento, fecha_alta):
        nuevo_fallero = Fallero(
            nombre=nombre,
            apellidos=apellidos,
            dni=dni,
            fecha_nacimiento=fecha_nacimiento,
            fecha_alta=fecha_alta,
            activo=True
        )
        with self.db_manager.get_db_session() as session:
            session.add(nuevo_fallero)
            session.commit()
        return nuevo_fallero

    def get_fallero_por_dni(self, dni):
        with self.db_manager.get_db_session() as session:
            return session.query(Fallero).filter_by(dni=dni).first()
