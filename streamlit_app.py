# ============================================================
# DASHBOARD - Sistema de Partners (SimiAI)
# Descripción: Dashboard analítico a través de Streamlit
# Autor: Fernando Raúl Robles
# Fecha: 04/11/2025
# ============================================================

# =============================
# IMPORTS PRINCIPALES
# =============================
import streamlit as st
import pandas as pd
import psycopg2
import plotly.express as px
import datetime

# Módulos personalizados
from src.db_connection import init_connection
from src.data_loader import load_data

# =============================
# CONFIG INICIAL
# =============================
st.set_page_config(page_title="Sistema de Partners", layout="wide")

# =============================
# CONEXIÓN Y CARGA DE DATOS
# =============================
st.sidebar.info("🔄 Cargando datos desde Neon.tech...")

# (1) Conexión
conn = None
try:
    conn = init_connection()
    with conn.cursor() as cur:
        cur.execute("SELECT NOW();")
        result = cur.fetchone()
    st.sidebar.success(f"🟢 Conectado a Neon.tech ({result[0]})")
except Exception as e:
    st.sidebar.warning(f"⚠️ No se pudo verificar NOW(): {e}")

# (2) Carga de dataframes
partners, countries, plans, statuses, notifications = load_data()
st.sidebar.success("🟢 Datos cargados correctamente")

# =============================
# PREPARACIÓN / MERGE
# =============================
merged = (
    partners
    .merge(countries, left_on="country_id", right_on="id_country", how="left")
    .merge(plans,     left_on="plan_id",    right_on="id_plan",    how="left")
    .merge(statuses,  left_on="status_id",  right_on="id_status",  how="left")
)

merged.rename(columns={
    "partner_name": "Partner",
    "country_name": "País",
    "plan_name":    "Plan",
    "status_name":  "Estado",
    "join_date":    "FechaAlta"
}, inplace=True)

