from dao.fallero_dao import FalleroDAO

class FalleroManager:
    def __init__(self, db_manager):
        self.fallero_dao = FalleroDAO(db_manager)

    def alta_fallero(self, nombre, apellidos, dni, fecha_nacimiento, fecha_alta):
        # Aquí se pueden añadir validaciones de negocio
        return self.fallero_dao.crear_fallero(nombre, apellidos, dni, fecha_nacimiento, fecha_alta)
