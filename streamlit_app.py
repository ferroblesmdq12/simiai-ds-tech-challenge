# ============================================================
# DASHBOARD - Sistema de Partners (SimiAI)
# Descripción: Dashboard analítico en Streamlit
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

# Importamos los módulos personalizados
from src.db_connection import init_connection
from src.data_loader import load_data

# =============================
# CONFIG INICIAL
# =============================
st.set_page_config(page_title="Sistema de Partners", layout="wide")

# ==================================
# CONEXIÓN A POSTGRESQL (Neon.tech)
# ==================================
st.sidebar.info("🔄 Cargando datos desde Neon.tech...")
partners, countries, plans, statuses, notifications = load_data()
st.sidebar.success("🟢 Datos cargados correctamente")

# =============================
# PREPARACIÓN / MERGE
# =============================
merged = (
    partners
    .merge(countries, left_on="country_id", right_on="id_country")
    .merge(plans, left_on="plan_id", right_on="id_plan")
    .merge(statuses, left_on="status_id", right_on="id_status")
)

merged.rename(columns={
    "partner_name": "Partner",
    "country_name": "País",
    "plan_name": "Plan",
    "status_name": "Estado",
    "join_date": "FechaAlta"
}, inplace=True)

merged["FechaAlta"] = pd.to_datetime(merged["FechaAlta"])

# =============================
# THEME / PALETA
# =============================
COLOR_PALETTE = ['#349ce4', '#1c4c74', '#6cb4e4', '#648cac', '#354551', '#b2b6b0']
BACKGROUND_COLOR = "#0E1117"
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

paises_unicos = sorted(merged["País"].unique().tolist())
opcion_pais = st.sidebar.selectbox(" País", ["Todos"] + paises_unicos)

planes_unicos = sorted(merged["Plan"].unique().tolist())
opcion_plan = st.sidebar.selectbox(" Plan Comercial", ["Todos"] + planes_unicos)

fecha_min = merged["FechaAlta"].min()
fecha_max = merged["FechaAlta"].max()
rango_fecha = st.sidebar.date_input(
    " Rango de Fecha de Alta",
    value=(fecha_min, fecha_max),
    min_value=fecha_min,
    max_value=fecha_max
)
fecha_inicio = pd.to_datetime(rango_fecha[0])
fecha_fin = pd.to_datetime(rango_fecha[1]) + pd.Timedelta(days=1)

# =============================
# FILTROS APLICADOS
# =============================
filtered = merged.copy()
if opcion_pais != "Todos":
    filtered = filtered[filtered["País"] == opcion_pais]
if opcion_plan != "Todos":
    filtered = filtered[filtered["Plan"] == opcion_plan]
filtered = filtered[(filtered["FechaAlta"] >= fecha_inicio) & (filtered["FechaAlta"] < fecha_fin)].copy()

notif_full = (
    notifications
    .merge(partners, left_on="partner_id", right_on="id_partner")
    .merge(plans, left_on="plan_id", right_on="id_plan")
)

# ============================================================
# HEADER
# ============================================================
st.markdown(
    """
    <h1 style="color:#E0E0E0; margin-bottom:0;">SimiAI - Sistema de Partners</h1>
    <p style="color:#b2b6b0; margin-top:4px;">
    Vista analítica ordenada desde el detalle más granular hacia la visión global.
    </p>
    """,
    unsafe_allow_html=True
)

# ============================================================
# NIVEL 1 — MICRO: DETALLE POR PLAN / PARTNER / INDUSTRIA
# ============================================================
st.markdown("<h2 style='color:#6cb4e4;'>🔍 Nivel 1 — Análisis Micro (Máxima Granularidad)</h2>", unsafe_allow_html=True)

col_plan, col_top, col_ind = st.columns(3)

# Partners activos por plan
activos_filtrados = filtered[filtered["Estado"] == "Activo"]
planes_counts = activos_filtrados.groupby("Plan")["Partner"].count().reset_index().rename(columns={"Partner": "PartnersActivos"})
fig_plan = px.bar(
    planes_counts, x="Plan", y="PartnersActivos", color="Plan",
    title="Partners Activos por Plan Comercial", color_discrete_sequence=COLOR_PALETTE
)
apply_dark_theme(fig_plan)
col_plan.plotly_chart(fig_plan, use_container_width=True)

# Top 10 partners por notificaciones
top_notif = notif_full.groupby("partner_name")["notification_count"].sum().reset_index().sort_values("notification_count", ascending=False).head(10)
fig_top = px.bar(
    top_notif, x="partner_name", y="notification_count", color="notification_count",
    title="Top 10 Partners por Notificaciones", color_continuous_scale="blues"
)
apply_dark_theme(fig_top)
col_top.plotly_chart(fig_top, use_container_width=True)

# Partners por industria
industria_counts = partners.groupby("industry")["id_partner"].count().reset_index().rename(columns={"industry": "Industria", "id_partner": "Cantidad"})
fig_ind = px.bar(
    industria_counts, x="Industria", y="Cantidad", color="Industria",
    title="Partners por Industria", text="Cantidad", color_discrete_sequence=COLOR_PALETTE
)
fig_ind.update_traces(textposition="outside")
apply_dark_theme(fig_ind)
col_ind.plotly_chart(fig_ind, use_container_width=True)

st.markdown("---")

# ============================================================
# NIVEL 2 — MEDIA: ESTADO Y DISTRIBUCIÓN POR PAÍS
# ============================================================
st.markdown("<h2 style='color:#6cb4e4;'>🌍 Nivel 2 — Análisis Medio (Segmentación)</h2>", unsafe_allow_html=True)
col_estado, col_geo = st.columns(2)

# Estado
estado_counts = filtered.assign(Activo=lambda df: df["Estado"] == "Activo").replace({True: "Activo", False: "No Activo"}).groupby("Activo")["Partner"].count().reset_index()
fig_estado = px.pie(estado_counts, names="Activo", values="Partner", title="Distribución de Estado (Activos vs No Activos)", color_discrete_sequence=COLOR_PALETTE)
apply_dark_theme(fig_estado)
col_estado.plotly_chart(fig_estado, use_container_width=True)

# País
geo_counts = filtered.groupby("País")["Partner"].count().reset_index().sort_values("Partner", ascending=True)
fig_geo = px.bar(
    geo_counts, x="Partner", y="País", orientation="h", text="Partner", color="País",
    title="Partners por País", color_discrete_sequence=COLOR_PALETTE
)
fig_geo.update_traces(textposition="outside")
apply_dark_theme(fig_geo)
col_geo.plotly_chart(fig_geo, use_container_width=True)

st.markdown("---")

# ============================================================
# NIVEL 3 — MEDIA-ALTA: TENDENCIA TEMPORAL
# ============================================================
st.markdown("<h2 style='color:#6cb4e4;'>📈 Nivel 3 — Tendencias y Crecimiento</h2>", unsafe_allow_html=True)
filtered["MesAlta"] = filtered["FechaAlta"].dt.to_period("M").astype(str)
evolucion = filtered.groupby("MesAlta")["Partner"].count().reset_index().rename(columns={"Partner": "NuevosPartners"})
fig_evol = px.line(evolucion, x="MesAlta", y="NuevosPartners", title="Evolución de Altas Mensuales", markers=True)
apply_dark_theme(fig_evol)
st.plotly_chart(fig_evol, use_container_width=True)

st.markdown("---")

# ============================================================
# NIVEL 4 — GLOBAL: RELACIONES ENTRE VARIABLES
# ============================================================
st.markdown("<h2 style='color:#6cb4e4;'>🔗 Nivel 4 — Relaciones Globales</h2>", unsafe_allow_html=True)
hoy = pd.Timestamp.now()
corr_df = notifications.merge(partners, left_on="partner_id", right_on="id_partner").merge(plans, left_on="plan_id", right_on="id_plan")
corr_df["FechaAlta"] = pd.to_datetime(corr_df["join_date"])
corr_df["AntiguedadMeses"] = ((hoy - corr_df["FechaAlta"]).dt.days / 30).round(1)
fig_corr = px.scatter(
    corr_df, x="AntiguedadMeses", y="notification_count", color="plan_name",
    title="Correlación entre Antigüedad y Notificaciones",
    labels={"AntiguedadMeses": "Antigüedad (meses)", "notification_count": "Notificaciones"},
    color_discrete_sequence=COLOR_PALETTE
)
apply_dark_theme(fig_corr)
st.plotly_chart(fig_corr, use_container_width=True)

st.markdown("---")

# ============================================================
# NIVEL 5 — MACRO: KPIs Y MAPA GLOBAL
# ============================================================
st.markdown("<h2 style='color:#6cb4e4;'>🌎 Nivel 5 — Visión Ejecutiva (Alta Granularidad)</h2>", unsafe_allow_html=True)
total_partners = len(filtered)
activos_partners = len(filtered[filtered["Estado"] == "Activo"])
prom_notif_global = notifications["notification_count"].mean().round(2)
col1, col2, col3 = st.columns(3)
col1.metric("Total Partners", total_partners)
col2.metric("Activos", activos_partners)
col3.metric("Promedio Notificaciones", prom_notif_global)

map_data = merged.groupby("País")["Partner"].count().reset_index().rename(columns={"Partner": "CantidadPartners"})
fig_map = px.choropleth(
    map_data, locations="País", locationmode="country names", color="CantidadPartners",
    color_continuous_scale="blues", title="Partners por País en América"
)
fig_map.update_layout(geo=dict(projection_type="natural earth", lonaxis_range=[-170, -30], lataxis_range=[-60, 75]))
apply_dark_theme(fig_map)
st.plotly_chart(fig_map, use_container_width=True)

st.markdown("---")

# ============================================================
# NIVEL 6 — INSIGHTS
# ============================================================
st.markdown("<h2 style='color:#6cb4e4;'>✅ Nivel 6 — Insights Clave</h2>", unsafe_allow_html=True)
st.markdown(
    """
    <ul style="color:#E0E0E0; font-size:15px; line-height:1.5;">
        <li>🔍 Los planes Premium y Enterprise concentran la mayor cantidad de partners activos.</li>
        <li>📈 El crecimiento mensual muestra una tendencia estable en los últimos períodos.</li>
        <li>🌎 Argentina, México y Colombia lideran en cantidad total de partners.</li>
        <li>💬 Existe correlación positiva entre antigüedad y cantidad de notificaciones, indicando mayor compromiso.</li>
    </ul>
    """,
    unsafe_allow_html=True
)
