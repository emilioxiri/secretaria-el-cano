import streamlit as st
import pandas as pd

class UIManager:
    
    @staticmethod
    def display_sidebar(username, logout_callback):
        """Muestra la barra lateral y devuelve la elección del menú."""
        with st.sidebar:
            st.write(f'Bienvenido *{username}*')
            logout_callback()
            st.title("🔥 Secretaría El Cano")
            return st.radio(
                "Menú de Navegación",
                ["Ver Falleros", "Añadir Fallero"]
            )

    @staticmethod
    def display_falleros_view(db_manager):
        """Muestra la vista principal con el listado y los filtros de falleros."""
        st.header("Listado de Falleros")

        with st.expander("🔎 Filtrar Falleros", expanded=False):
            col1, col2, col3 = st.columns(3)
            with col1:
                filtro_nombre = st.text_input("Filtrar por Nombre:")
            with col2:
                filtro_apellidos = st.text_input("Filtrar por Apellidos:")
            with col3:
                filtro_activos = st.selectbox("Filtrar por Estado:", ["Todos", "Activos", "Inactivos"])

        falleros = db_manager.get_filtered_falleros(filtro_nombre, filtro_apellidos, filtro_activos)

        if not falleros:
            st.info("No se encontraron falleros con los filtros seleccionados.")
        else:
            df_falleros = pd.DataFrame([vars(f) for f in falleros])
            df_falleros = df_falleros.drop(columns=['_sa_instance_state'])
            st.dataframe(df_falleros, use_container_width=True, hide_index=True)
            st.write(f"Total de falleros mostrados: {len(df_falleros)}")

    @staticmethod
    def display_add_fallero_view():
        """Muestra el formulario para añadir un nuevo fallero."""
        st.header("Añadir Nuevo Fallero")
        # Aquí irá el formulario para añadir un nuevo fallero
        st.info("Formulario de alta en construcción.")

    # ... Aquí se añadirían métodos para las otras vistas (modificar, etc.)