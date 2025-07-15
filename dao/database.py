import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from contextlib import contextmanager

from models.fallero import Fallero
from models.usuario import Usuario

class DatabaseManager:
    def __init__(self):
        db_url = os.getenv(
            "DATABASE_URL",
            "mysql+mysqlconnector://root:nolasabrasnunca1970@localhost:3306/secretaria-el-cano"
        )
        self.engine = create_engine(db_url)
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)

    @contextmanager
    def get_db_session(self):
        db = self.SessionLocal()
        try:
            yield db
        finally:
            db.close()

    def get_all_users(self) -> list[Usuario]:
        with self.get_db_session() as db:
            return db.query(Usuario).all()

    def get_filtered_falleros(self, nombre, apellidos, estado):
        with self.get_db_session() as db:
            query = db.query(Fallero)
            if nombre:
                query = query.filter(Fallero.nombre.like(f"%{nombre}%"))
            if apellidos:
                query = query.filter(Fallero.apellidos.like(f"%{apellidos}%"))
            if estado == "Activos":
                query = query.filter(Fallero.activo == True)
            elif estado == "Inactivos":
                query = query.filter(Fallero.activo == False)
            return query.all()