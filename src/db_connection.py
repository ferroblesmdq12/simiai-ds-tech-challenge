# ===========================================
# db_connection.py
# Módulo de conexión a Neon.tech PostgreSQL
# Autor: Fernando Raúl Robles
# ===========================================

import streamlit as st
import psycopg2
import time

def init_connection(retries=3, delay=2):
    """Crea una conexión a Neon.tech con reintentos automáticos."""
    for attempt in range(retries):
        try:
            conn = psycopg2.connect(
                host="ep-red-feather-aca9j4sc-pooler.sa-east-1.aws.neon.tech",
                database="partnersdb",
                user="neondb_owner",
                password="npg_U7EYlIQ6XZPO",
                port="5432",
                sslmode="require"
            )
            return conn
        except Exception as e:
            st.sidebar.warning(f"Intento {attempt+1}/{retries} fallido: {e}")
            time.sleep(delay)
    st.sidebar.error("❌ No se pudo conectar con Neon.tech tras varios intentos.")
    return None


