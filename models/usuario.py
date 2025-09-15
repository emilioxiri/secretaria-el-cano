"""
Usuario model definition for the Secretaria El Cano application.

This module defines the Usuario entity which represents system users with authentication capabilities.
"""

from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class Usuario(Base):
    """
    Usuario entity representing a system user with authentication capabilities.
    
    This model stores user authentication information and access control data.
    
    Attributes:
        id: Primary key identifier for the user.
        nombre: Display name of the user.
        email: Email address used for authentication (must be unique).
        hashed_password: Bcrypt hashed password for authentication.
        activo: Boolean flag indicating if the user account is active.
    """
    
    __tablename__ = "Usuario"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    activo = Column(Boolean, default=True)

    def __repr__(self) -> str:
        """Return string representation of the Usuario instance."""
        return f"<Usuario(id={self.id}, email='{self.email}', activo={self.activo})>"
    
    @property
    def is_active(self) -> bool:
        """Return whether the user account is active."""
        return self.activo