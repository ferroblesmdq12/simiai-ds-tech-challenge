# ====================================================
# DASHBOARD - Sistema de Partners (SimiAI)
# Descripción: Dashboard analítico para visualización
# atravéz de "Streamlit".
# Autor: Fernando Raúl Robles
# Fecha: 25/10/2025
# ====================================================

import streamlit as st
import pandas as pd
import psycopg2
import plotly.express as px

# =============================
# CONFIGURACIÓN INICIAL
# =============================
st.set_page_config(page_title="Sistema de Partners - SimiAI", layout="wide")

# ==============================================
# CONEXIÓN A POSTGRESQL LOCAL (no se utilizará)
# ==============================================
# def connect_db():
#     try:
#         conn = psycopg2.connect(
#             host="localhost",
#             database="partnersdb",
#             user="postgres",
#             password="ferdata",  
#             port=5432
#         )
#         return conn
#     except Exception as e:
#         st.error(f"Error de conexión: {e}")
#         return None

# conn = connect_db()

# ==============================================
# CONEXIÓN A POSTGRESQL en la nube (neon.tech)
# ==============================================

def connect_db():
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
        st.error(f"Error de conexión: {e}")
        return None
conn = connect_db()

# =============================
# CARGA DE DATOS
# =============================
@st.cache_data
def load_data():
    partners = pd.read_sql("SELECT * FROM partners;", conn)
    countries = pd.read_sql("SELECT * FROM countries;", conn)
    plans = pd.read_sql("SELECT * FROM plans;", conn)
    statuses = pd.read_sql("SELECT * FROM statuses;", conn)
    notifications = pd.read_sql("SELECT * FROM notifications;", conn)
    return partners, countries, plans, statuses, notifications

partners, countries, plans, statuses, notifications = load_data()

# =============================
# MERGE DE DATOS PARA ANÁLISIS
# =============================
merged = (
    partners
    .merge(countries, left_on="country_id", right_on="id_country")
    .merge(plans, left_on="plan_id", right_on="id_plan")
    .merge(statuses, left_on="status_id", right_on="id_status")
)

merged.rename(columns={
    "country_name": "País",
    "plan_name": "Plan",
    "status_name": "Estado",
    "partner_name": "Partner"
}, inplace=True)

# =============================
# INTERFAZ DE USUARIO
# =============================
st.title("📊 Dashboardo — Sistema de Partners (SimiAI)")
st.markdown("Visualización de métricas clave sobre partners, planes, países y actividad.")

col1, col2, col3 = st.columns(3)

# Paleta de colores personalizada (Blue Dashboard)
COLOR_PALETTE = ['#354551', '#1c4c74', '#349ce4', '#6cb4e4', '#648cac', '#b2b6b0']



# KPI 1: Partners activos por plan
active = merged[merged["Estado"] == "Activo"]
kpi1 = active.groupby("Plan")["Partner"].count().reset_index()
fig1 = px.bar(kpi1, x="Plan", y="Partner", color="Plan", title="Partners Activos por Plan", color_discrete_sequence=COLOR_PALETTE)

# KPI 2: Altas mensuales
merged["join_month"] = pd.to_datetime(merged["join_date"]).dt.to_period("M").astype(str)
kpi2 = merged.groupby("join_month")["Partner"].count().reset_index()
fig2 = px.line(kpi2, x="join_month", y="Partner", title="Evolución de Altas Mensuales")


# KPI 3: Distribución geográfica (gráfico de barras horizontales)
kpi3 = merged.groupby("País")["Partner"].count().reset_index().sort_values("Partner", ascending=True)
fig3 = px.bar(
    kpi3,
    x="Partner",
    y="País",
    orientation="h",
    text="Partner",
    color="País",
    title="Distribución de Partners por País",
    color_discrete_sequence=COLOR_PALETTE
)

fig3.update_traces(textposition="outside")
fig3.update_layout(
    xaxis_title="Cantidad de Partners",
    yaxis_title="País",
    showlegend=False,
    plot_bgcolor="white",
    xaxis=dict(showgrid=True, gridcolor="lightgray"),
)

# st.plotly_chart(fig3, use_container_width=True)

# Mostrar KPIs en columnas

col1.plotly_chart(fig1, use_container_width=True)
col2.plotly_chart(fig2, use_container_width=True)
col3.plotly_chart(fig3, use_container_width=True)

# KPI 4: Promedio de notificaciones por plan
notif = notifications.merge(partners, left_on="partner_id", right_on="id_partner").merge(plans, left_on="plan_id", right_on="id_plan")
kpi4 = notif.groupby("plan_name")["notification_count"].agg(["sum", "mean"]).reset_index()
fig4 = px.bar(kpi4, x="plan_name", y="mean", color="plan_name", title="Promedio de Notificaciones por Plan", color_discrete_sequence=COLOR_PALETTE)

# KPI 5: Top 10 partners por notificaciones
kpi5 = notif.groupby("partner_name")["notification_count"].sum().reset_index().sort_values("notification_count", ascending=False).head(10)
fig5 = px.bar(kpi5, x="partner_name", y="notification_count", color="notification_count", title="Top 10 Partners por Notificaciones", color_continuous_scale=COLOR_PALETTE  # degradado azul elegante)
              

st.plotly_chart(fig4, use_container_width=True)
st.plotly_chart(fig5, use_container_width=True)

# =============================
# CONCLUSIÓN
# =============================
st.markdown("---")
st.markdown("✅ **Interpretaciones sugeridas:**")
st.markdown("""
- Los planes *Premium* y *Enterprise* concentran la mayor cantidad de partners activos.  
- El crecimiento mensual muestra tendencia positiva hasta septiembre.  
- Argentina, México y Colombia lideran la cantidad de partners en LATAM.  
- El promedio de notificaciones por plan confirma una mayor actividad en Enterprise.  
""")
