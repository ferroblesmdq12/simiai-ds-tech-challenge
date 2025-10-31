# ===========================================
# db_connection.py
# Módulo de conexión a Neon.tech PostgreSQL
# Autor: Fernando Raúl Robles
# ===========================================

import psycopg2
import streamlit as st
import time

# =============================
# FUNCIÓN PRINCIPAL DE CONEXIÓN
# =============================
def connect_db():
    """Establece conexión directa a Neon.tech PostgreSQL."""
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
        st.error(f"❌ Error de conexión: {e}")
        return None


# =============================
# FUNCIÓN PARA INICIALIZAR CONEXIÓN
# =============================
def init_connection():
    """
    Usa session_state para mantener una conexión persistente.
    Reconecta automáticamente si la sesión de Neon está en pausa.
    """
    if "conn" not in st.session_state or st.session_state.conn is None:
        st.session_state.conn = connect_db()

    conn = st.session_state.conn

    if conn is not None:
        try:
            cur = conn.cursor()
            cur.execute("SELECT NOW();")
            cur.close()
            st.sidebar.success("🟢 Conectado a Neon.tech")
        except (Exception, psycopg2.InterfaceError):
            st.sidebar.warning("🔄 Reconectando con Neon...")
            time.sleep(3)
            st.session_state.conn = connect_db()
            conn = st.session_state.conn
    else:
        st.sidebar.error("❌ No se pudo establecer conexión con la base de datos.")

    return conn
