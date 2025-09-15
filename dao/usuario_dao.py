"""
Usuario Data Access Object for the Secretaria El Cano application.

This module provides data access operations for Usuario entities,
including user creation and retrieval operations.
"""

import bcrypt
from typing import Optional
from models.usuario import Usuario
from dao.database import DatabaseManager


class UsuarioDAO:
    """
    Data Access Object for Usuario entity operations.
    
    This class provides methods for creating, retrieving, and managing
    user data in the database with proper password hashing.
    """
    
    def __init__(self, db_manager: DatabaseManager):
        """
        Initialize the UsuarioDAO with a database manager.
        
        Args:
            db_manager: Database manager instance for database operations.
        """
        self.db_manager = db_manager

    def crear_usuario(self, nombre: str, email: str, plain_password: str) -> Usuario:
        """
        Create a new user with hashed password.
        
        Args:
            nombre: Display name for the user.
            email: Email address for authentication (must be unique).
            plain_password: Plain text password to be hashed.
            
        Returns:
            The created Usuario instance.
            
        Raises:
            Exception: If there's an error during user creation or email already exists.
        """
        hashed_password = bcrypt.hashpw(
            plain_password.encode('utf-8'), 
            bcrypt.gensalt()
        ).decode('utf-8')
        
        nuevo_usuario = Usuario(
            nombre=nombre,
            email=email,
            hashed_password=hashed_password,
            activo=True
        )
        
        with self.db_manager.get_db_session() as session:
            session.add(nuevo_usuario)
            session.commit()
            session.refresh(nuevo_usuario)
            
        return nuevo_usuario

    def get_usuario_por_email(self, email: str) -> Optional[Usuario]:
        """
        Retrieve a user by email address.
        
        Args:
            email: Email address to search for.
            
        Returns:
            Usuario instance if found, None otherwise.
        """
        with self.db_manager.get_db_session() as session:
            return session.query(Usuario).filter_by(email=email).first()
    
    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """
        Verify a plain password against a hashed password.
        
        Args:
            plain_password: Plain text password to verify.
            hashed_password: Stored hashed password to compare against.
            
        Returns:
            True if passwords match, False otherwise.
        """
        return bcrypt.checkpw(
            plain_password.encode('utf-8'), 
            hashed_password.encode('utf-8')
        )
