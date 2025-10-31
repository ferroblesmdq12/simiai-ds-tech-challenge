# ===========================================
# data_loader.py
# Módulo para carga de datos desde Neon.tech
# Autor: Fernando Raúl Robles
# ===========================================

import pandas as pd
import streamlit as st
from src.db_connection import init_connection

@st.cache_data(ttl=600)
def load_data():
    """Lee todas las tablas desde Neon.tech con reconexión automática."""
    try:
        conn = init_connection()
        if not conn:
            raise Exception("No se pudo abrir conexión a Neon.tech")

        partners = pd.read_sql("SELECT * FROM partners;", conn)
        countries = pd.read_sql("SELECT * FROM countries;", conn)
        plans = pd.read_sql("SELECT * FROM plans;", conn)
        statuses = pd.read_sql("SELECT * FROM statuses;", conn)
        notifications = pd.read_sql("SELECT * FROM notifications;", conn)
        conn.close()

        return partners, countries, plans, statuses, notifications

    except Exception as e:
        st.error(f"⚠️ Error al leer tablas desde Neon.tech: {e}")
        # Retorna DataFrames vacíos pero con columnas esperadas (evita KeyError)
        return (
            pd.DataFrame(columns=["id_partner", "partner_name", "country_id", "plan_id", "status_id", "join_date"]),
            pd.DataFrame(columns=["id_country", "country_name"]),
            pd.DataFrame(columns=["id_plan", "plan_name"]),
            pd.DataFrame(columns=["id_status", "status_name"]),
            pd.DataFrame(columns=["partner_id", "notification_date", "notification_count"])
        )