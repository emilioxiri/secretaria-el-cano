import os
import streamlit as st
from sqlalchemy.exc import OperationalError
from models.fallero import Base as FalleroBase
from models.usuario import Base as UsuarioBase
from dao.database import DatabaseManager
from managers.auth_manager import AuthManager
from managers.ui_manager import UIManager
from sqlalchemy import text

def db_init(db_manager):
    init_db = os.getenv("INIT_DB", "False") == "True"
    if init_db:
        # Crear todas las tablas
        FalleroBase.metadata.create_all(db_manager.engine)
        UsuarioBase.metadata.create_all(db_manager.engine)
    else:
        # Comprobar si la base de datos existe
        try:
            with db_manager.get_db_session() as session:
                session.execute(text('SELECT 1'))
        except OperationalError:
            st.error("La base de datos no existe. Define INIT_DB=True para crearla.")
            st.stop()

class SecretariaElCanoApp:
    def __init__(self):
        st.set_page_config(page_title="Secretaría El Cano", page_icon="🔥", layout="wide")
        self.db_manager = DatabaseManager()
        db_init(self.db_manager)
        self.auth_manager = AuthManager(self.db_manager)
        self.ui_manager = UIManager()

    def run(self):
        usuarios = self.db_manager.get_all_users()
        usuarios_activos = [u for u in usuarios if getattr(u, "activo", True)]
        
        if not usuarios_activos:
            st.error("No hay usuarios activos en la base de datos. Contacta con el administrador.")
            return

        self.auth_manager.login()
        if st.session_state["authentication_status"] is None:
            st.info("Por favor, inicia sesión.")
        elif st.session_state["authentication_status"] is False:
            st.error("Login fallido. Verifica tus credenciales.")
        elif st.session_state["authentication_status"] is True:
            self._show_main_app(st.session_state["name"])
            
    def _show_main_app(self, name):
        """Muestra la aplicación principal después del login."""
        # Usar el nombre recibido, no session_state
        menu_choice = self.ui_manager.display_sidebar(
            username=name or "Usuario",
            logout_callback=self.auth_manager.logout
        )

        if menu_choice == "Ver Falleros":
            self.ui_manager.display_falleros_view(self.db_manager)
        
        elif menu_choice == "Añadir Fallero":
            self.ui_manager.display_add_fallero_view()
        
        # ... Aquí irían las llamadas a otros métodos de la UI
        else:
            st.write("Selecciona una opción del menú.")

if __name__ == "__main__":
    app = SecretariaElCanoApp()
    app.run()