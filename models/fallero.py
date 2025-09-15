"""
Fallero model definition for the Secretaria El Cano application.

This module defines the Fallero entity which represents a member of the falla organization.
"""

from sqlalchemy import Boolean, Column, Date, Integer, String
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class Fallero(Base):
    """
    Fallero entity representing a member of the falla organization.
    
    This model stores information about falla members including personal details,
    registration dates, and status.
    
    Attributes:
        id: Primary key identifier for the fallero.
        nombre: First name of the fallero.
        apellidos: Last names of the fallero.
        dni: Spanish national identification number (DNI).
        fecha_nacimiento: Date of birth.
        fecha_alta: Registration date in the organization.
        activo: Boolean flag indicating if the fallero is active.
    """
    
    __tablename__ = "Fallero"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(100), nullable=False)
    apellidos = Column(String(255), nullable=False)
    dni = Column(String(20), unique=True, nullable=False)
    fecha_nacimiento = Column(Date, nullable=False)
    fecha_alta = Column(Date, nullable=False)
    activo = Column(Boolean, default=True)

    def __repr__(self) -> str:
        """Return string representation of the Fallero instance."""
        return f"<Fallero(id={self.id}, nombre='{self.nombre}', apellidos='{self.apellidos}')>"
    
    @property
    def full_name(self) -> str:
        """Return the full name of the fallero."""
        return f"{self.nombre} {self.apellidos}"
