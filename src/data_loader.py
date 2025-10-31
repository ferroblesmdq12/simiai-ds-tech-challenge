# ===========================================
# data_loader.py
# Módulo para carga de datos desde Neon.tech
# Autor: Fernando Raúl Robles
# ===========================================

import streamlit as st
import pandas as pd
from src.db_connection import init_connection


@st.cache_data(ttl=300)
def load_data():
    """Carga los datos desde Neon usando la conexión cacheada."""
    conn = init_connection()
    if conn is None:
        st.error("❌ No se pudo establecer conexión con Neon.tech")
        return [pd.DataFrame()] * 5

    try:
        partners = pd.read_sql("SELECT * FROM partners;", conn)
        countries = pd.read_sql("SELECT * FROM countries;", conn)
        plans = pd.read_sql("SELECT * FROM plans;", conn)
        statuses = pd.read_sql("SELECT * FROM statuses;", conn)
        notifications = pd.read_sql("SELECT * FROM notifications;", conn)
        return partners, countries, plans, statuses, notifications
    except Exception as e:
        st.error(f"⚠️ Error al cargar datos: {e}")
        return [pd.DataFrame()] * 5