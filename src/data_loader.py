# ===========================================
# data_loader.py
# Módulo para carga de datos desde Neon.tech
# Autor: Fernando Raúl Robles
# ===========================================

# src/data_loader.py
import streamlit as st
import pandas as pd
from src.db_connection import init_connection

@st.cache_data(ttl=300)
def load_data():
    """Carga los datos desde Neon usando la conexión cacheada."""
    conn = init_connection()  # usa la conexión global cacheada
    partners = pd.read_sql("SELECT * FROM partners;", conn)
    countries = pd.read_sql("SELECT * FROM countries;", conn)
    plans = pd.read_sql("SELECT * FROM plans;", conn)
    statuses = pd.read_sql("SELECT * FROM statuses;", conn)
    notifications = pd.read_sql("SELECT * FROM notifications;", conn)
    return partners, countries, plans, statuses, notifications
