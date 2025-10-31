# ===========================================
# data_loader.py
# Módulo para carga de datos desde Neon.tech
# Autor: Fernando Raúl Robles
# ===========================================

import streamlit as st
import pandas as pd
from src.db_connection import init_connection
import psycopg2

@st.cache_data(ttl=300)
def load_data():
    """Carga los datos desde Neon.tech, reintentando si la conexión fue cerrada."""
    try:
        conn = init_connection()

        #  Verificamos que la conexión esté viva
        if conn is None or conn.closed != 0:
            st.warning("♻️ Conexión cerrada, reabriendo...")
            conn = init_connection()

        #  Leemos las tablas
        partners = pd.read_sql("SELECT * FROM partners;", conn)
        countries = pd.read_sql("SELECT * FROM countries;", conn)
        plans = pd.read_sql("SELECT * FROM plans;", conn)
        statuses = pd.read_sql("SELECT * FROM statuses;", conn)
        notifications = pd.read_sql("SELECT * FROM notifications;", conn)

        return partners, countries, plans, statuses, notifications

    except psycopg2.InterfaceError as e:
        st.error(f"⚠️ Conexión interrumpida con Neon.tech: {e}")
        return [pd.DataFrame()] * 5

    except Exception as e:
        st.error(f"⚠️ Error al leer tablas desde Neon.tech: {e}")
        return [pd.DataFrame()] * 5
