"""
Authentication manager module for the Secretaria El Cano application.

This module handles user authentication using streamlit-authenticator
and manages user sessions.
"""

from typing import Tuple, Optional
import streamlit as st
import streamlit_authenticator as stauth
from dao.database import DatabaseManager
from dao.usuario_dao import UsuarioDAO
from constants.messages import AuthTranslations, Messages
from config.settings import settings


class AuthManager:
    """
    Authentication manager for handling user login and logout operations.
    
    This class manages user authentication using streamlit-authenticator
    and integrates with the database to validate user credentials.
    """
    
    def __init__(self, db_manager: DatabaseManager):
        """
        Initialize the authentication manager.
        
        Args:
            db_manager: Database manager instance for user operations.
        """
        self.db_manager = db_manager
        self.usuario_dao = UsuarioDAO(db_manager)
        self.authenticator = self._setup_authenticator()
        
    def _setup_authenticator(self) -> stauth.Authenticate:
        """
        Set up the streamlit authenticator with user credentials.
        
        Returns:
            Configured streamlit authenticator instance.
        """
        users = self.db_manager.get_all_users()
        credentials = {
            "usernames": {
                user.email: {
                    "name": user.email,
                    "password": user.hashed_password,
                }
                for user in users if user.activo
            }
        }
        
        auth_config = settings.get_auth_config()
        return stauth.Authenticate(
            credentials,
            auth_config.cookie_name,
            auth_config.secret_key,
            cookie_expiry_days=auth_config.cookie_expiry_days,
        )

    def login(self) -> Optional[Tuple[Optional[str], Optional[bool], Optional[str]]]:
        """
        Display the login widget and handle user authentication.
        
        Returns:
            Tuple containing authentication result (name, status, username).
        """
        app_config = settings.get_app_config()
        st.image(app_config.logo_path, width=180)
        return self.authenticator.login("main", fields=AuthTranslations.LOGIN_FORM)

    def logout(self, location: str = 'sidebar') -> None:
        """
        Display the logout widget and handle user logout.
        
        Args:
            location: Where to display the logout button ('sidebar' or 'main').
        """
        return self.authenticator.logout(Messages.AUTH_LOGOUT, location=location)