import os
import streamlit as st
from sqlalchemy.exc import OperationalError
from models.fallero import Base as FalleroBase
from models.usuario import Base as UsuarioBase
from dao.database import DatabaseManager
from managers.auth_manager import AuthManager
from managers.ui_manager import UIManager
from sqlalchemy import text
from constants.messages import Messages
from config.settings import settings
from utils.logger import get_logger

# Initialize logger
logger = get_logger(__name__)

def db_init(db_manager: DatabaseManager) -> None:
    """
    Initialize the database based on configuration settings.
    
    Args:
        db_manager: Database manager instance for handling database operations.
        
    Raises:
        OperationalError: When database doesn't exist and INIT_DB is False.
    """
    logger.info("Initializing database connection")
    
    if settings.database.init_db:
        logger.info("Creating database tables")
        # Create all tables
        FalleroBase.metadata.create_all(db_manager.engine)
        UsuarioBase.metadata.create_all(db_manager.engine)
        logger.info("Database tables created successfully")
    else:
        # Check if database exists
        try:
            with db_manager.get_db_session() as session:
                session.execute(text('SELECT 1'))
            logger.info("Database connection verified")
        except OperationalError as e:
            logger.error(f"Database connection failed: {e}")
            st.error(Messages.DB_NOT_EXISTS)
            st.stop()

class SecretariaElCanoApp:
    """
    Main application class for the Secretaria El Cano management system.
    
    This class orchestrates the entire application flow including authentication,
    database initialization, and UI management.
    """
    
    def __init__(self):
        """Initialize the application with configuration and managers."""
        logger.info("Starting Secretaria El Cano application")
        
        app_config = settings.get_app_config()
        st.set_page_config(
            page_title=app_config.app_name, 
            page_icon=app_config.app_icon, 
            layout=app_config.layout
        )
        
        self.db_manager = DatabaseManager()
        db_init(self.db_manager)
        self.auth_manager = AuthManager(self.db_manager)
        self.ui_manager = UIManager()
        
        logger.info("Application initialized successfully")

    def run(self) -> None:
        """
        Run the main application flow.
        
        Handles user authentication and displays appropriate content based on
        authentication status.
        """
        usuarios = self.db_manager.get_all_users()
        usuarios_activos = [u for u in usuarios if getattr(u, "activo", True)]
        
        if not usuarios_activos:
            st.error(Messages.AUTH_NO_ACTIVE_USERS)
            return

        self.auth_manager.login()
        if st.session_state["authentication_status"] is None:
            st.info(Messages.AUTH_LOGIN_REQUIRED)
        elif st.session_state["authentication_status"] is False:
            st.error(Messages.AUTH_LOGIN_FAILED)
        elif st.session_state["authentication_status"] is True:
            self._show_main_app(st.session_state["name"])
            
    def _show_main_app(self, name: str) -> None:
        """
        Display the main application interface after successful authentication.
        
        Args:
            name: Username of the authenticated user.
        """
        menu_choice = self.ui_manager.display_sidebar(
            username=name or "Usuario",
            logout_callback=self.auth_manager.logout
        )

        if menu_choice == Messages.MENU_VIEW_FALLEROS:
            self.ui_manager.display_falleros_view(self.db_manager)

        elif menu_choice == Messages.MENU_VIEW_USERS:
            self.ui_manager.display_usuarios_view(self.db_manager)
        
        elif menu_choice == Messages.MENU_ADD_FALLERO:
            self.ui_manager.display_add_fallero_view(self.db_manager)
        
        else:
            st.write(Messages.MENU_SELECT_OPTION)

if __name__ == "__main__":
    app = SecretariaElCanoApp()
    app.run()