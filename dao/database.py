"""
Database manager module for the Secretaria El Cano application.

This module provides database connectivity and basic CRUD operations
for the application entities.
"""

from datetime import datetime
from typing import List, Optional
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from contextlib import contextmanager

from models.fallero import Fallero
from models.usuario import Usuario
from config.settings import settings


class DatabaseManager:
    """
    Database manager class providing database connectivity and operations.
    
    This class handles database connections, session management, and provides
    methods for common database operations on application entities.
    """
    
    def __init__(self):
        """Initialize database manager with connection from settings."""
        db_config = settings.get_database_config()
        self.engine = create_engine(db_config.url)
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)

    @contextmanager
    def get_db_session(self):
        """
        Context manager for database sessions.
        
        Provides a database session that is automatically closed after use.
        
        Yields:
            Session: SQLAlchemy database session.
        """
        db = self.SessionLocal()
        try:
            yield db
        finally:
            db.close()

    def get_all_users(self) -> List[Usuario]:
        """
        Retrieve all users from the database.
        
        Returns:
            List of Usuario instances.
        """
        with self.get_db_session() as db:
            return db.query(Usuario).all()

    def get_filtered_falleros(self, nombre: Optional[str] = None, 
                            apellidos: Optional[str] = None, 
                            estado: Optional[str] = None) -> List[Fallero]:
        """
        Retrieve falleros with optional filtering.
        
        Args:
            nombre: Optional filter by first name (partial match).
            apellidos: Optional filter by last names (partial match).
            estado: Optional filter by status ("Activos", "Inactivos", or None for all).
            
        Returns:
            List of Fallero instances matching the filters.
        """
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

    def insert_fallero(self, nombre: str, apellidos: str, dni: str, 
                      fecha_nacimiento) -> Fallero:
        """
        Insert a new fallero into the database.
        
        Args:
            nombre: First name of the fallero.
            apellidos: Last names of the fallero.
            dni: Spanish national identification number.
            fecha_nacimiento: Date of birth.
            
        Returns:
            The created Fallero instance.
            
        Raises:
            Exception: If there's an error during database insertion.
        """
        with self.get_db_session() as db:
            nuevo_fallero = Fallero(
                nombre=nombre,
                apellidos=apellidos,
                dni=dni,
                fecha_nacimiento=fecha_nacimiento,
                fecha_alta=datetime.now().date(),
                activo=True
            )
            db.add(nuevo_fallero)
            db.commit()
            db.refresh(nuevo_fallero)
            return nuevo_fallero

