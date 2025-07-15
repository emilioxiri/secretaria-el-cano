from sqlalchemy import Boolean, Column, Date, Integer, String
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Fallero(Base):
    __tablename__ = "Fallero"
    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(100), nullable=False)
    apellidos = Column(String(255), nullable=False)
    dni = Column(String(20), unique=True, nullable=False)
    fecha_nacimiento = Column(Date, nullable=False)
    fecha_alta = Column(Date, nullable=False)
    activo = Column(Boolean, default=True)
