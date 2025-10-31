# # # ====================================================
# # # DASHBOARD - Sistema de Partners (SimiAI)
# # # Descripción: Dashboard analítico para visualización
# # # atravéz de "Streamlit".
# # # Autor: Fernando Raúl Robles
# # # Fecha: 27/10/2025
# # # ====================================================

# =============================
# IMPORTS PRINCIPALES
# =============================

import streamlit as st
import pandas as pd
import psycopg2
import plotly.express as px
import datetime

# Importamos los módulos personalizados
from src.db_connection import init_connection
from src.data_loader import load_data


# =============================
# CONFIG INICIAL
# =============================
st.set_page_config(
    page_title="Sistema de Partners",
    layout="wide"
)


# ==================================
# CONEXIÓN A POSTGRESQL (Neon.tech)
# ==================================

conn = init_connection()

if conn:
    st.sidebar.success("🟢 Conectado a Neon.tech")
else:
    st.sidebar.error("❌ No se pudo establecer conexión con la base de datos.")


# =============================
# CARGA DE DATOS
# =============================

# Limpieza manual opcional de caché (solo durante desarrollo)
# st.cache_data.clear()

partners, countries, plans, statuses, notifications = load_data()




# =============================
# PREPARACIÓN / MERGE
# =============================
merged = (
    partners
    .merge(countries, left_on="country_id", right_on="id_country")
    .merge(plans,     left_on="plan_id",     right_on="id_plan")
    .merge(statuses,  left_on="status_id",   right_on="id_status")
)

merged.rename(columns={
    "partner_name": "Partner",
    "country_name": "País",
    "plan_name":    "Plan",
    "status_name":  "Estado",
    "join_date":    "FechaAlta"
}, inplace=True)

merged["FechaAlta"] = pd.to_datetime(merged["FechaAlta"])

# =============================
# THEME / PALETA
# =============================
COLOR_PALETTE = ['#349ce4', '#1c4c74', '#6cb4e4', '#648cac', '#354551', '#b2b6b0']
BACKGROUND_COLOR = "#0E1117"   # fondo oscuro estilo Streamlit dark
TEXT_COLOR = "#E0E0E0"
GRID_COLOR = "#333"

def apply_dark_theme(fig):
    fig.update_layout(
        paper_bgcolor=BACKGROUND_COLOR,
        plot_bgcolor=BACKGROUND_COLOR,
        font=dict(color=TEXT_COLOR),
        title_font=dict(size=18, color="#6cb4e4"),
        xaxis=dict(color=TEXT_COLOR, gridcolor=GRID_COLOR),
        yaxis=dict(color=TEXT_COLOR, gridcolor=GRID_COLOR),
        legend=dict(font=dict(color=TEXT_COLOR))
    )
    return fig

# =============================
# SIDEBAR: FILTROS
# =============================
st.sidebar.header("Filtros")

# Filtro País
paises_unicos = sorted(merged["País"].unique().tolist())
opcion_pais = st.sidebar.selectbox(
    " País",
    options=["Todos"] + paises_unicos,
    index=0
)

# Filtro Plan
planes_unicos = sorted(merged["Plan"].unique().tolist())
opcion_plan = st.sidebar.selectbox(
    " Plan Comercial",
    options=["Todos"] + planes_unicos,
    index=0
)

# Filtro Rango de Fechas
fecha_min = merged["FechaAlta"].min()
fecha_max = merged["FechaAlta"].max()

rango_fecha = st.sidebar.date_input(
    " Rango de Fecha de Alta",
    value=(fecha_min, fecha_max),
    min_value=fecha_min,
    max_value=fecha_max
)

# Normalizamos types del filtro de fechas
fecha_inicio = pd.to_datetime(rango_fecha[0])
fecha_fin    = pd.to_datetime(rango_fecha[1]) + pd.Timedelta(days=1)  # incluye fin

# =============================
# APLICAMOS LOS FILTROS
# =============================
filtered = merged.copy()

if opcion_pais != "Todos":
    filtered = filtered[filtered["País"] == opcion_pais]

if opcion_plan != "Todos":
    filtered = filtered[filtered["Plan"] == opcion_plan]

filtered = filtered[
    (filtered["FechaAlta"] >= fecha_inicio) &
    (filtered["FechaAlta"] <  fecha_fin)
].copy()

# Para panel operativo usamos notif + partners originales (sin filtro de país/plan),
# pero si querés también filtrar por país/plan necesitaríamos mergear notif con filtered.
notif_full = (
    notifications
    .merge(partners, left_on="partner_id", right_on="id_partner")
    .merge(plans,    left_on="plan_id",    right_on="id_plan")
)

# =============================
# HEADER (título)
# =============================
st.markdown(
    f"""
    <h1 style="color:#E0E0E0; margin-bottom:0;"> SimiAI - Sistema de Partners </h1>
    <p style="color:#b2b6b0; margin-top:4px;">
    Vista ejecutiva y operativa de la red de partners. <br/>
    Los filtros de la izquierda impactan en todas las métricas excepto las operativas globales de notificaciones.
    </p>
    """,
    unsafe_allow_html=True
)

# ============================================================
# FECHA Y HORA DE ACTUALIZACIÓN (hora local del visitante)
# ============================================================
st.components.v1.html(
    """
    <div id="update-time" style="color:#6cb4e4; font-size:14px; margin-top:-10px;">
        🔄 Actualizando datos...
    </div>
    <script>
        // Esperamos unos segundos para simular carga de datos
        setTimeout(() => {
            const now = new Date();
            const options = {
                year: 'numeric', month: '2-digit', day: '2-digit',
                hour: '2-digit', minute: '2-digit', second: '2-digit'
            };
            const localTime = now.toLocaleString([], options);
            document.getElementById("update-time").innerHTML = 
                "📅 Datos actualizados al " + localTime;
        }, 1500);
    </script>
    """,
    height=40
)


# ============================================================
# NIVEL 1 — VISIÓN GENERAL (tarjetas KPI)
# ============================================================

total_partners      = len(filtered)
activos_partners    = len(filtered[filtered["Estado"] == "Activo"])
inactivos_partners  = len(filtered[filtered["Estado"] != "Activo"])
prom_notif_global   = notifications["notification_count"].mean().round(2)

col_kpi1, col_kpi2, col_kpi3, col_kpi4 = st.columns(4)

with col_kpi1:
    st.metric(" Total de Partners", total_partners)

with col_kpi2:
    st.metric(" Partners Activos", activos_partners)

with col_kpi3:
    st.metric(" Partners No Activos", inactivos_partners)

with col_kpi4:
    st.metric(" Promedio Notificaciones (global)", prom_notif_global)

st.markdown("---")

# ============================================================
# NIVEL 2 — DISTRIBUCIÓN ALTA NIVEL
#    - Estado (Activos vs No Activos)
#    - Distribución geográfica
# ============================================================

col_dist1, col_dist2 = st.columns(2)

# 2A. Estado (pie activos vs no activos)
estado_counts = (
    filtered
    .assign(Activo=lambda df: df["Estado"] == "Activo")
    .replace({True: "Activo", False: "No Activo"})
    .groupby("Activo")["Partner"]
    .count()
    .reset_index()
    .rename(columns={"Partner": "Cantidad", "Activo": "Estado"})
)

fig_estado = px.pie(
    estado_counts,
    names="Estado",
    values="Cantidad",
    title="Distribución Partners Activos vs No Activos",
    color_discrete_sequence=COLOR_PALETTE
)
fig_estado.update_traces(textinfo="percent+label", pull=[0.05, 0.05])
apply_dark_theme(fig_estado)
col_dist1.plotly_chart(fig_estado, use_container_width=True)

# 2B. Distribución geográfica (barras horizontales)
geo_counts = (
    filtered
    .groupby("País")["Partner"]
    .count()
    .reset_index()
    .sort_values("Partner", ascending=True)
)

fig_geo = px.bar(
    geo_counts,
    x="Partner",
    y="País",
    orientation="h",
    text="Partner",
    color="País",
    title="Partners por País",
    color_discrete_sequence=COLOR_PALETTE,
    labels={"Partner": "Cantidad de Partners", "País": "País"}
)
fig_geo.update_traces(textposition="outside")
apply_dark_theme(fig_geo)
col_dist2.plotly_chart(fig_geo, use_container_width=True)

st.markdown("---")

# ============================================================
# NIVEL 3 — EVOLUCIÓN TEMPORAL / TENDENCIA
#    - Altas mensuales
# ============================================================

filtered["MesAlta"] = filtered["FechaAlta"].dt.to_period("M").astype(str)
evolucion = (
    filtered
    .groupby("MesAlta")["Partner"]
    .count()
    .reset_index()
    .rename(columns={"Partner": "NuevosPartners"})
    .sort_values("MesAlta")
)

fig_evol = px.line(
    evolucion,
    x="MesAlta",
    y="NuevosPartners",
    title="Evolución de Altas Mensuales",
    markers=True,
    labels={"MesAlta": "Mes de Alta", "NuevosPartners": "Cantidad de Nuevos Partners"}
)
fig_evol.update_traces(line_color="#349ce4", marker_color="#6cb4e4")
apply_dark_theme(fig_evol)

st.plotly_chart(fig_evol, use_container_width=True)

st.markdown("---")

# ============================================================
# NIVEL 4 — ANÁLISIS POR PLAN Y TOP PARTNERS
# ============================================================

col_plan, col_top = st.columns(2)

# 4A. Partners activos por plan (solo filtrados)
activos_filtrados = filtered[filtered["Estado"] == "Activo"]
planes_counts = (
    activos_filtrados
    .groupby("Plan")["Partner"]
    .count()
    .reset_index()
    .rename(columns={"Partner": "PartnersActivos"})
    .sort_values("PartnersActivos", ascending=False)
)

fig_plan = px.bar(
    planes_counts,
    x="Plan",
    y="PartnersActivos",
    color="Plan",
    title="Partners Activos por Plan Comercial",
    color_discrete_sequence=COLOR_PALETTE,
    labels={"Plan": "Plan Comercial", "PartnersActivos": "Partners Activos"}
)
apply_dark_theme(fig_plan)
col_plan.plotly_chart(fig_plan, use_container_width=True)

# 4B. Top 10 partners por notificaciones (global)
top_notif = (
    notif_full
    .groupby("partner_name")["notification_count"]
    .sum()
    .reset_index()
    .sort_values("notification_count", ascending=False)
    .head(10)
)
fig_top = px.bar(
    top_notif,
    x="partner_name",
    y="notification_count",
    color="notification_count",
    title="Top 10 Partners por Volumen de Notificaciones",
    color_continuous_scale=COLOR_PALETTE,
    labels={"partner_name": "Partner", "notification_count": "Total Notificaciones"}
)
apply_dark_theme(fig_top)
col_top.plotly_chart(fig_top, use_container_width=True)

st.markdown("---")

# ============================================================
# INSIGHTS FINALES
# ============================================================
st.markdown(
    "<h3 style='color:#6cb4e4;'>✅ Insights Clave</h3>",
    unsafe_allow_html=True
)

st.markdown(
    """
    <ul style="color:#E0E0E0; font-size:15px; line-height:1.5;">
        <li>Los planes Premium y Enterprise concentran la mayor cantidad de partners activos<li>
        <li>El crecimiento mensual muestra una tendencia positiva entre abril y septiembre<li>
        <li>Argentina, México y Colombia lideran en cantidad de partners activos<li>
        <li>Los planes de mayor costo presentan más notificaciones, indicando mayor compromiso<li>
        <li>Se identifican oportunidades de expansión en países con menor representación<li>

    </ul>
    """,
    unsafe_allow_html=True
)
