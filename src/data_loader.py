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
    try:
        conn = init_connection()

        partners = pd.read_sql("SELECT * FROM partners;", conn)
        countries = pd.read_sql("SELECT * FROM countries;", conn)
        plans = pd.read_sql("SELECT * FROM plans;", conn)
        statuses = pd.read_sql("SELECT * FROM statuses;", conn)
        notifications = pd.read_sql("SELECT * FROM notifications;", conn)

        conn.close()
        return partners, countries, plans, statuses, notifications

    except Exception as e:
        st.warning("♻️ Reconectando a Neon.tech...")
        try:
            conn = init_connection()
            partners = pd.read_sql("SELECT * FROM partners;", conn)
            countries = pd.read_sql("SELECT * FROM countries;", conn)
            plans = pd.read_sql("SELECT * FROM plans;", conn)
            statuses = pd.read_sql("SELECT * FROM statuses;", conn)
            notifications = pd.read_sql("SELECT * FROM notifications;", conn)
            conn.close()
            return partners, countries, plans, statuses, notifications
        except Exception as err:
            st.error(f"⚠️ Error al leer tablas desde Neon.tech: {err}")
            return pd.DataFrame(), pd.DataFrame(), pd.DataFrame(), pd.DataFrame(), pd.DataFrame()
