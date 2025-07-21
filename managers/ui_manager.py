import streamlit as st
import pandas as pd

from dao.database import DatabaseManager

class UIManager:
    @staticmethod
    def set_responsive_layout():
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
    def display_sidebar(username, logout_callback):
        """Muestra la barra lateral y devuelve la elección del menú."""
        with st.sidebar:
            st.write(f'Bienvenido *{username}*')
            logout_callback()
            st.title("🔥 Secretaría El Cano")
            return st.radio(
                "Menú de Navegación",
                ["Ver Falleros", "Añadir Fallero", "Ver Usuarios"]
            )

    @staticmethod
    def display_falleros_view(db_manager):
        st.header("Listado de Falleros")
        with st.expander("🔎 Filtrar Falleros", expanded=False):
            col1, col2, col3 = st.columns([1, 1, 1])
            with col1:
                filtro_nombre = st.text_input("Filtrar por Nombre:", key="filtro_nombre")
            with col2:
                filtro_apellidos = st.text_input("Filtrar por Apellidos:", key="filtro_apellidos")
            with col3:
                filtro_activos = st.selectbox("Filtrar por Estado:", ["Todos", "Activos", "Inactivos"], key="filtro_estado")
        falleros = db_manager.get_filtered_falleros(filtro_nombre, filtro_apellidos, filtro_activos)
        if not falleros:
            st.info("No se encontraron falleros con los filtros seleccionados.")
        else:
            df_falleros = pd.DataFrame([vars(f) for f in falleros])
            df_falleros = df_falleros.drop(columns=['_sa_instance_state'])
            # Limitar el ancho de la tabla usando container
            with st.container():
                st.dataframe(df_falleros, use_container_width=True, hide_index=True)
                UIManager.set_responsive_layout()
            st.write(f"Total de falleros mostrados: {len(df_falleros)}")

    @staticmethod
    def display_add_fallero_view(db_manager: DatabaseManager):
        UIManager.set_responsive_layout()
        st.header("Añadir Fallero/a")
        with st.form("add_fallero_form", clear_on_submit=True):
            # Limitar el ancho de los inputs usando columns
            col1, col2 = st.columns([1, 1])
            with col1:
                nombre = st.text_input("Nombre*", max_chars=50, key="nombre")
                dni = st.text_input("DNI*", max_chars=9, help="Formato: 8 números y una letra (ej: 12345678A)", key="dni")
            with col2:
                apellidos = st.text_input("Apellidos*", max_chars=100, key="apellidos")
                fecha_nacimiento = st.date_input("Fecha de nacimiento*", format="YYYY-MM-DD", key="fecha_nacimiento")
            submitted = st.form_submit_button("Añadir Fallero")
            if submitted:
                errores = UIManager.validate_fallero_inputs(nombre, apellidos, dni)
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
                        st.success("Fallero añadido correctamente.")
                    except Exception as e:
                        st.error(f"Error al insertar el fallero: {e}")

    @staticmethod
    def display_usuarios_view(db_manager: DatabaseManager):
        UIManager.set_responsive_layout()
        st.header("Listado de Usuarios")

        # Filtros
        with st.expander("🔎 Filtrar Usuarios", expanded=False):
            col1, col2, col3 = st.columns([1, 1, 1])
            with col1:
                filtro_nombre = st.text_input("Filtrar por Nombre de usuario:", key="filtro_usuario_nombre")
            with col2:
                filtro_email = st.text_input("Filtrar por Email:", key="filtro_usuario_email")
            with col3:
                filtro_activo = st.selectbox("Filtrar por Estado:", ["Todos", "Activos", "Inactivos"], key="filtro_usuario_estado")

        # Botón para añadir usuario
        st.markdown(
            """
            <style>
            .add-user-btn { float: right; margin-top: -50px; margin-bottom: 10px; }
            </style>
            """,
            unsafe_allow_html=True,
        )
        if st.button("➕", key="add_user_btn", help="Añadir usuario", use_container_width=False):
            st.session_state["show_add_user_popup"] = True

        # Obtener y filtrar usuarios
        usuarios = db_manager.get_all_users()
        usuarios_filtrados = []
        for u in usuarios:
            if filtro_nombre and filtro_nombre.lower() not in (u.username or "").lower():
                continue
            if filtro_email and filtro_email.lower() not in (u.email or "").lower():
                continue
            if filtro_activo == "Activos" and not getattr(u, "activo", True):
                continue
            if filtro_activo == "Inactivos" and getattr(u, "activo", True):
                continue
            usuarios_filtrados.append(u)

        if not usuarios_filtrados:
            st.info("No se encontraron usuarios con los filtros seleccionados.")
        else:
            df_usuarios = pd.DataFrame([vars(u) for u in usuarios_filtrados])
            if "_sa_instance_state" in df_usuarios.columns:
                df_usuarios = df_usuarios.drop(columns=['_sa_instance_state'])
            st.dataframe(df_usuarios, use_container_width=True, hide_index=True)
            st.write(f"Total de usuarios mostrados: {len(df_usuarios)}")

        # Popup para añadir usuario
        if st.session_state.get("show_add_user_popup", False):
            UIManager.display_add_usuario_popup(db_manager)

    @staticmethod
    def display_add_usuario_popup(db_manager: DatabaseManager):
        with st.popover("Añadir nuevo usuario"):
            username = st.text_input("Nombre de usuario*", key="nuevo_usuario_username")
            email = st.text_input("Email*", key="nuevo_usuario_email")
            password = st.text_input("Contraseña*", type="password", key="nuevo_usuario_password")
            activo = st.checkbox("Activo", value=True, key="nuevo_usuario_activo")
            submitted = st.button("Crear usuario", key="crear_usuario_btn")
            if submitted:
                errores = UIManager.validate_usuario_inputs(username, email, password)
                if errores:
                    for err in errores:
                        st.error(err)
                else:
                    try:
                        db_manager.insert_usuario(
                            username=username.strip(),
                            email=email.strip().lower(),
                            password=password,
                            activo=activo
                        )
                        st.success("Usuario añadido correctamente.")
                        st.session_state["show_add_user_popup"] = False
                    except Exception as e:
                        st.error(f"Error al insertar el usuario: {e}")

            if st.button("Cancelar", key="cancelar_usuario_btn"):
                st.session_state["show_add_user_popup"] = False

    @staticmethod
    def validate_fallero_inputs(nombre, apellidos, dni):
        errores = []
        if not nombre.strip():
            errores.append("El nombre es obligatorio.")
        if not apellidos.strip():
            errores.append("Los apellidos son obligatorios.")
        if not dni.strip() or len(dni) != 9 or not dni[:8].isdigit() or not dni[8].isalpha():
            errores.append("El DNI debe tener 8 números y una letra (ej: 12345678A).")
        return errores

    @staticmethod
    def validate_usuario_inputs(username, email, password):
        errores = []
        if not username.strip():
            errores.append("El nombre de usuario es obligatorio.")
        if not email.strip() or "@" not in email or "." not in email:
            errores.append("El email debe tener un formato válido.")
        if not password or len(password) < 6:
            errores.append("La contraseña debe tener al menos 6 caracteres.")
        return errores