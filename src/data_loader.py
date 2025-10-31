# ===========================================
# data_loader.py
# Módulo para carga de datos desde Neon.tech
# Autor: Fernando Raúl Robles
# ===========================================

import streamlit as st
import pandas as pd
import psycopg2
from src.db_connection import init_connection

@st.cache_data(ttl=300)
def load_data():
    """Carga los datos desde Neon.tech, reconectando si es necesario."""
    conn = init_connection()
    if conn is None:
        st.error("❌ No se pudo establecer conexión con Neon.tech.")
        return [pd.DataFrame()] * 5

    # 🔁 Verificamos si la conexión sigue activa
    try:
        cur = conn.cursor()
        cur.execute("SELECT 1;")
        cur.close()
    except psycopg2.InterfaceError:
        st.warning("♻️ Reconectando a Neon.tech...")
        conn = init_connection()

    try:
        partners = pd.read_sql("SELECT * FROM partners;", conn)
        countries = pd.read_sql("SELECT * FROM countries;", conn)
        plans = pd.read_sql("SELECT * FROM plans;", conn)
        statuses = pd.read_sql("SELECT * FROM statuses;", conn)
        notifications = pd.read_sql("SELECT * FROM notifications;", conn)
        return partners, countries, plans, statuses, notifications

    except Exception as e:
        st.error(f"⚠️ Error al cargar datos desde Neon.tech: {e}")
        return [pd.DataFrame()] * 5
