# ===========================================
# db_connection.py
# Módulo de conexión a Neon.tech PostgreSQL
# Autor: Fernando Raúl Robles
# ===========================================

import streamlit as st
import psycopg2

@st.cache_resource
def init_connection():
    """Crea una conexión persistente a Neon.tech"""
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
        st.error(f"❌ Error creando conexión: {e}")
        return None


