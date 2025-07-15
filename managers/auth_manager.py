from typing import Tuple
import streamlit as st
import streamlit_authenticator as stauth
from dao.database import DatabaseManager
from dao.usuario_dao import UsuarioDAO
from utils.translations import login_translations

class AuthManager:
    def __init__(self, db_manager: DatabaseManager):
        self.db_manager = db_manager
        self.usuario_dao = UsuarioDAO(db_manager)
        self.authenticator = self._setup_authenticator()
        
    def _setup_authenticator(self):
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
                
        return stauth.Authenticate(
            credentials,
            "falla_cookie",
            "auth_secret_key",
            cookie_expiry_days=1,
        )

    def login(self) -> (Tuple[str | None, bool | None, str | None] | None):
        """Muestra el widget de login y devuelve el estado."""
        st.image("assets/logo.png", width=180)
        return self.authenticator.login("main", fields=login_translations)

    def logout(self, location='sidebar'):
        """Muestra el widget de logout."""
        return self.authenticator.logout("Cerrar Sesión", location=location)