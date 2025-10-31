# ===========================================
# data_loader.py
# Módulo para carga de datos desde Neon.tech
# Autor: Fernando Raúl Robles
# ===========================================

import pandas as pd
import streamlit as st

# =============================
# FUNCIÓN DE CARGA DE DATOS
# =============================

@st.cache_data(ttl=300)
def load_data():
    """
    Carga todas las tablas desde la base partnersdb (Neon.tech)
    y las devuelve como DataFrames de pandas.
    Se ejecuta dentro del contexto de la app principal.
    """
    # ⚠️ Importamos aquí la conexión para evitar el paso de objetos no serializables
    from src.db_connection import init_connection
    conn = init_connection()

    try:
        partners = pd.read_sql("SELECT * FROM partners;", conn)
        countries = pd.read_sql("SELECT * FROM countries;", conn)
        plans = pd.read_sql("SELECT * FROM plans;", conn)
        statuses = pd.read_sql("SELECT * FROM statuses;", conn)
        notifications = pd.read_sql("SELECT * FROM notifications;", conn)

        st.sidebar.info("📊 Datos cargados correctamente desde Neon.tech")

        return partners, countries, plans, statuses, notifications

    except Exception as e:
        st.error(f"❌ Error al cargar datos: {e}")
        return None, None, None, None, None

    finally:
        if conn:
            conn.close()
