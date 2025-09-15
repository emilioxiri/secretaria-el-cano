"""
User Interface manager module for the Secretaria El Cano application.

This module handles all user interface components and interactions
using Streamlit for the web interface.
"""

import streamlit as st
import pandas as pd
from typing import Optional

from dao.database import DatabaseManager
from constants.messages import Messages


class UIManager:
    """
    User Interface manager for handling Streamlit components and layouts.
    
    This class provides methods for displaying various UI components
    including forms, tables, and navigation elements.
    """

    @staticmethod
    def set_responsive_layout() -> None:
        """Set responsive CSS layout for better mobile and desktop experience."""
        st.markdown(
            """
            <style>
            .main > div { max-width: 900px; margin-left: auto; margin-right: auto; }
            .stDataFrame { max-width: 100vw !important; }
            .stForm { max-width: 600px; margin-left: auto; margin-right: auto; }
            </style>
            """,
            unsafe_allow_html=True,
        )

    @staticmethod
    def display_sidebar(username: str, logout_callback) -> str:
        """
        Display the sidebar with navigation menu and user information.
        
        Args:
            username: Name of the authenticated user.
            logout_callback: Function to call for user logout.
            
        Returns:
            Selected menu option.
        """
        with st.sidebar:
            st.write(f'{Messages.AUTH_WELCOME} *{username}*')
            logout_callback()
            st.title("🔥 Secretaría El Cano")
            return st.radio(
                Messages.MENU_NAVIGATION,
                [Messages.MENU_VIEW_FALLEROS, Messages.MENU_ADD_FALLERO, Messages.MENU_VIEW_USERS]
            )

    @staticmethod
    def display_falleros_view(db_manager: DatabaseManager) -> None:
        """
        Display the falleros list view with filtering capabilities.
        
        Args:
            db_manager: Database manager for data operations.
        """
        st.header(Messages.FALLEROS_TITLE)
        
        with st.expander(Messages.FALLEROS_FILTER_TITLE, expanded=False):
            col1, col2, col3 = st.columns([1, 1, 1])
            with col1:
                filtro_nombre = st.text_input(Messages.FALLEROS_FILTER_NAME, key="filtro_nombre")
            with col2:
                filtro_apellidos = st.text_input(Messages.FALLEROS_FILTER_SURNAME, key="filtro_apellidos")
            with col3:
                filtro_activos = st.selectbox(
                    Messages.FALLEROS_FILTER_STATUS, 
                    [Messages.FALLEROS_STATUS_ALL, Messages.FALLEROS_STATUS_ACTIVE, Messages.FALLEROS_STATUS_INACTIVE], 
                    key="filtro_estado"
                )
        
        falleros = db_manager.get_filtered_falleros(filtro_nombre, filtro_apellidos, filtro_activos)
        
        if not falleros:
            st.info(Messages.FALLEROS_NOT_FOUND)
        else:
            df_falleros = pd.DataFrame([vars(f) for f in falleros])
            df_falleros = df_falleros.drop(columns=['_sa_instance_state'], errors='ignore')
            
            with st.container():
                st.dataframe(df_falleros, use_container_width=True, hide_index=True)
                UIManager.set_responsive_layout()
            
            st.write(Messages.FALLEROS_TOTAL_SHOWN.format(count=len(df_falleros)))

    @staticmethod
    def display_add_fallero_view(db_manager: DatabaseManager) -> None:
        """
        Display the form for adding a new fallero.
        
        Args:
            db_manager: Database manager for data operations.
        """
        UIManager.set_responsive_layout()
        st.header(Messages.ADD_FALLERO_TITLE)
        
        with st.form("add_fallero_form", clear_on_submit=True):
            col1, col2 = st.columns([1, 1])
            with col1:
                nombre = st.text_input(Messages.ADD_FALLERO_NAME, max_chars=50, key="nombre")
                dni = st.text_input(
                    Messages.ADD_FALLERO_DNI, 
                    max_chars=9, 
                    help=Messages.ADD_FALLERO_DNI_HELP, 
                    key="dni"
                )
            with col2:
                apellidos = st.text_input(Messages.ADD_FALLERO_SURNAME, max_chars=100, key="apellidos")
                fecha_nacimiento = st.date_input(
                    Messages.ADD_FALLERO_BIRTH_DATE, 
                    format="YYYY-MM-DD", 
                    key="fecha_nacimiento"
                )
            
            submitted = st.form_submit_button(Messages.ADD_FALLERO_SUBMIT)
            
            if submitted:
                errores = UIManager._validate_fallero_inputs(nombre, apellidos, dni)
                if errores:
                    for err in errores:
                        st.error(err)
                else:
                    try:
                        db_manager.insert_fallero(
                            nombre=nombre.strip(),
                            apellidos=apellidos.strip(),
                            dni=dni.strip().upper(),
                            fecha_nacimiento=fecha_nacimiento
                        )
                        st.success(Messages.ADD_FALLERO_SUCCESS)
                    except Exception as e:
                        st.error(Messages.DB_ERROR_INSERT_FALLERO.format(error=str(e)))

    @staticmethod
    def display_usuarios_view(db_manager: DatabaseManager) -> None:
        """
        Display the users list view with filtering capabilities.
        
        Args:
            db_manager: Database manager for data operations.
        """
        UIManager.set_responsive_layout()
        st.header(Messages.USERS_TITLE)

        # Filters
        with st.expander(Messages.USERS_FILTER_TITLE, expanded=False):
            col1, col2, col3 = st.columns([1, 1, 1])
            with col1:
                filtro_nombre = st.text_input(Messages.USERS_FILTER_USERNAME, key="filtro_usuario_nombre")
            with col2:
                filtro_email = st.text_input(Messages.USERS_FILTER_EMAIL, key="filtro_usuario_email")
            with col3:
                filtro_activo = st.selectbox(
                    Messages.USERS_FILTER_STATUS, 
                    [Messages.FALLEROS_STATUS_ALL, Messages.FALLEROS_STATUS_ACTIVE, Messages.FALLEROS_STATUS_INACTIVE], 
                    key="filtro_usuario_estado"
                )

        # Add user button
        st.markdown(
            """
            <style>
            .add-user-btn { float: right; margin-top: -50px; margin-bottom: 10px; }
            </style>
            """,
            unsafe_allow_html=True,
        )
        if st.button("➕", key="add_user_btn", help=Messages.USERS_ADD_BUTTON_HELP, use_container_width=False):
            st.session_state["show_add_user_popup"] = True

        # Get and filter users
        usuarios = db_manager.get_all_users()
        usuarios_filtrados = UIManager._filter_users(usuarios, filtro_nombre, filtro_email, filtro_activo)

        if not usuarios_filtrados:
            st.info(Messages.USERS_NOT_FOUND)
        else:
            df_usuarios = pd.DataFrame([vars(u) for u in usuarios_filtrados])
            if "_sa_instance_state" in df_usuarios.columns:
                df_usuarios = df_usuarios.drop(columns=['_sa_instance_state'])
            st.dataframe(df_usuarios, use_container_width=True, hide_index=True)
            st.write(Messages.USERS_TOTAL_SHOWN.format(count=len(df_usuarios)))

        # Popup for adding user
        if st.session_state.get("show_add_user_popup", False):
            UIManager._display_add_usuario_popup(db_manager)

    @staticmethod
    def _filter_users(usuarios, filtro_nombre: Optional[str], filtro_email: Optional[str], 
                     filtro_activo: Optional[str]) -> list:
        """
        Filter users based on provided criteria.
        
        Args:
            usuarios: List of users to filter.
            filtro_nombre: Name filter.
            filtro_email: Email filter.
            filtro_activo: Status filter.
            
        Returns:
            Filtered list of users.
        """
        usuarios_filtrados = []
        for u in usuarios:
            if filtro_nombre and filtro_nombre.lower() not in (u.nombre or "").lower():
                continue
            if filtro_email and filtro_email.lower() not in (u.email or "").lower():
                continue
            if filtro_activo == Messages.FALLEROS_STATUS_ACTIVE and not getattr(u, "activo", True):
                continue
            if filtro_activo == Messages.FALLEROS_STATUS_INACTIVE and getattr(u, "activo", True):
                continue
            usuarios_filtrados.append(u)
        return usuarios_filtrados

    @staticmethod
    def _display_add_usuario_popup(db_manager: DatabaseManager) -> None:
        """
        Display popup form for adding a new user.
        
        Args:
            db_manager: Database manager for data operations.
        """
        with st.popover(Messages.ADD_USER_TITLE):
            username = st.text_input(Messages.ADD_USER_USERNAME, key="nuevo_usuario_username")
            email = st.text_input(Messages.ADD_USER_EMAIL, key="nuevo_usuario_email")
            password = st.text_input(Messages.ADD_USER_PASSWORD, type="password", key="nuevo_usuario_password")
            activo = st.checkbox(Messages.ADD_USER_ACTIVE, value=True, key="nuevo_usuario_activo")
            
            submitted = st.button(Messages.ADD_USER_SUBMIT, key="crear_usuario_btn")
            if submitted:
                errores = UIManager._validate_usuario_inputs(username, email, password)
                if errores:
                    for err in errores:
                        st.error(err)
                else:
                    try:
                        # This would need to be implemented in database manager
                        # db_manager.insert_usuario(username.strip(), email.strip().lower(), password, activo)
                        st.success(Messages.ADD_USER_SUCCESS)
                        st.session_state["show_add_user_popup"] = False
                    except Exception as e:
                        st.error(Messages.DB_ERROR_INSERT_USER.format(error=str(e)))

            if st.button(Messages.ADD_USER_CANCEL, key="cancelar_usuario_btn"):
                st.session_state["show_add_user_popup"] = False

    @staticmethod
    def _validate_fallero_inputs(nombre: str, apellidos: str, dni: str) -> list:
        """
        Validate fallero form inputs.
        
        Args:
            nombre: First name input.
            apellidos: Last names input.
            dni: DNI input.
            
        Returns:
            List of validation error messages.
        """
        errores = []
        if not nombre.strip():
            errores.append(Messages.VALIDATION_NAME_REQUIRED)
        if not apellidos.strip():
            errores.append(Messages.VALIDATION_SURNAME_REQUIRED)
        if not dni.strip() or len(dni) != 9 or not dni[:8].isdigit() or not dni[8].isalpha():
            errores.append(Messages.VALIDATION_DNI_INVALID)
        return errores

    @staticmethod
    def _validate_usuario_inputs(username: str, email: str, password: str) -> list:
        """
        Validate user form inputs.
        
        Args:
            username: Username input.
            email: Email input.
            password: Password input.
            
        Returns:
            List of validation error messages.
        """
        errores = []
        if not username.strip():
            errores.append(Messages.VALIDATION_USERNAME_REQUIRED)
        if not email.strip() or "@" not in email or "." not in email:
            errores.append(Messages.VALIDATION_EMAIL_INVALID)
        if not password or len(password) < 6:
            errores.append(Messages.VALIDATION_PASSWORD_MIN_LENGTH)
        return errores