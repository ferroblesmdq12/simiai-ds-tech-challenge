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

from src.data_loader import load_data

st.sidebar.info("🔄 Cargando datos desde Neon.tech...")
partners, countries, plans, statuses, notifications = load_data()
st.sidebar.success("🟢 Datos cargados correctamente")

# =============================
# CARGA DE DATOS
# =============================

test_query = "SELECT NOW();"
try:
    cur = conn.cursor()
    cur.execute(test_query)
    result = cur.fetchone()
    cur.close()
    st.sidebar.success(f"🟢 Conectado a Neon.tech ({result[0]})")

except psycopg2.InterfaceError:
    st.sidebar.warning("♻️ Conexión cerrada, reabriendo...")
    try:
        conn = init_connection()
        cur = conn.cursor()
        cur.execute(test_query)
        result = cur.fetchone()
        cur.close()
        st.sidebar.success(f"🟢 Reconectado a Neon.tech ({result[0]})")
    except Exception as e:
        st.sidebar.error(f"❌ Error reconectando a Neon.tech: {e}")

except Exception as e:
    st.sidebar.error(f"⚠️ Error verificando conexión: {e}")

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

# ============================================================
# CREACIÓN DE DATAFRAMES DERIVADOS (ANTES DE USARLOS)
# ============================================================

# Aseguramos columna MesAlta y DataFrame evolución
if not filtered.empty and "FechaAlta" in filtered.columns:
    filtered["MesAlta"] = filtered["FechaAlta"].dt.to_period("M").astype(str)
    evolucion = (
        filtered.groupby("MesAlta")["Partner"]
        .count()
        .reset_index()
        .rename(columns={"Partner": "NuevosPartners"})
        .sort_values("MesAlta")
    )
else:
    evolucion = pd.DataFrame(columns=["MesAlta", "NuevosPartners"])


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

# # ============================================================
# # NIVEL 1B — KPIs AVANZADOS Y CORRELACIÓN DE VARIABLES
# # ============================================================

# st.markdown(
#     "<h3 style='color:#6cb4e4;'>📊 Indicadores Avanzados y Relaciones</h3>",
#     unsafe_allow_html=True
# )

# # ========================================
# # KPI 1 — Tasa de Crecimiento Mensual (%)
# # ========================================
# # Tomamos las altas mensuales (ya creadas en 'evolucion')
# if len(evolucion) >= 2:
#     altas_mes_actual = evolucion["NuevosPartners"].iloc[-1]
#     altas_mes_prev = evolucion["NuevosPartners"].iloc[-2]
#     tasa_crecimiento = ((altas_mes_actual - altas_mes_prev) / altas_mes_prev) * 100 if altas_mes_prev > 0 else 0
# else:
#     tasa_crecimiento = 0

# # ========================================
# # KPI 2 — Antigüedad Promedio de Partners (meses)
# # ========================================
# hoy = pd.Timestamp.now()
# filtered["AntiguedadMeses"] = ((hoy - filtered["FechaAlta"]).dt.days / 30).round(1)
# antiguedad_prom = filtered["AntiguedadMeses"].mean().round(1)

# # ========================================
# # KPI 3 — País con Más Altas Recientes
# # ========================================
# # Consideramos el último mes disponible en 'evolucion'
# if not filtered.empty:
#     mes_reciente = filtered["FechaAlta"].dt.to_period("M").max()
#     ultimas_altas = filtered[filtered["FechaAlta"].dt.to_period("M") == mes_reciente]
#     pais_top = ultimas_altas["País"].value_counts().idxmax()
#     altas_top = ultimas_altas["País"].value_counts().max()
# else:
#     pais_top, altas_top = "Sin datos", 0

# # ========================================
# # VISUALIZACIÓN DE KPIs (tarjetas)
# # ========================================
# col_kpiA, col_kpiB, col_kpiC = st.columns(3)

# with col_kpiA:
#     st.metric(
#         "📈 Tasa de Crecimiento Mensual",
#         f"{tasa_crecimiento:.1f}%",
#         delta=f"{altas_mes_actual - altas_mes_prev:+d} altas vs mes previo"
#     )

# with col_kpiB:
#     st.metric(
#         "🕓 Antigüedad Promedio",
#         f"{antiguedad_prom} meses",
#         delta=None
#     )

# with col_kpiC:
#     st.metric(
#         "🌍 País con Más Altas Recientes",
#         f"{pais_top} ({altas_top})",
#         delta=None
#     )

# st.markdown("---")

# # ============================================================
# # GRÁFICO DE CORRELACIÓN — Antigüedad vs Notificaciones
# # ============================================================

# st.markdown(
#     "<h4 style='color:#6cb4e4;'>🔗 Relación entre Antigüedad y Nivel de Actividad</h4>",
#     unsafe_allow_html=True
# )

# # Mergeamos con notifications para obtener 'notification_count'
# corr_df = (
#     notifications
#     .merge(partners, left_on="partner_id", right_on="id_partner")
#     .merge(plans, left_on="plan_id", right_on="id_plan")
# )

# # Calculamos antigüedad y aseguramos columnas numéricas
# corr_df["FechaAlta"] = pd.to_datetime(corr_df["join_date"])
# corr_df["AntiguedadMeses"] = ((hoy - corr_df["FechaAlta"]).dt.days / 30).round(1)

# # Creamos scatter con tendencia
# fig_corr = px.scatter(
#     corr_df,
#     x="AntiguedadMeses",
#     y="notification_count",
#     color="plan_name",
#     trendline="ols",
#     title="Correlación entre Antigüedad del Partner y Notificaciones",
#     labels={
#         "AntiguedadMeses": "Antigüedad (meses)",
#         "notification_count": "Cantidad de Notificaciones",
#         "plan_name": "Plan"
#     },
#     color_discrete_sequence=COLOR_PALETTE
# )

# apply_dark_theme(fig_corr)
# st.plotly_chart(fig_corr, use_container_width=True)


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
# NIVEL 5 — DISTRIBUCIÓN DE PARTNERS POR INDUSTRIA
# ============================================================

st.markdown(
    "<h3 style='color:#6cb4e4;'>🏭 Distribución de Partners por Industria</h3>",
    unsafe_allow_html=True
)

# Agrupamos los partners por industria
industria_counts = (
    partners
    .groupby("industry")["id_partner"]
    .count()
    .reset_index()
    .rename(columns={"industry": "Industria", "id_partner": "Cantidad"})
    .sort_values("Cantidad", ascending=False)
)

# Creamos el gráfico
fig_industria = px.bar(
    industria_counts,
    x="Industria",
    y="Cantidad",
    color="Industria",
    title="Cantidad de Partners por Industria",
    text="Cantidad",
    color_discrete_sequence=COLOR_PALETTE
)

fig_industria.update_traces(textposition="outside")
apply_dark_theme(fig_industria)
st.plotly_chart(fig_industria, use_container_width=True)


# ============================================================
# NIVEL 6 — MAPA GEOGRÁFICO DE PARTNERS EN AMÉRICA
# ============================================================

st.markdown(
    "<h3 style='color:#6cb4e4;'>🌎 Distribución Geográfica de Partners en América</h3>",
    unsafe_allow_html=True
)

# Agrupamos cantidad de partners por país
map_data = (
    merged.groupby("País")["Partner"]
    .count()
    .reset_index()
    .rename(columns={"Partner": "CantidadPartners"})
)

# Corrección opcional de nombres de países
map_data["País"] = map_data["País"].replace({
    "Estados Unidos": "United States of America",
    "USA": "United States",
    "México": "Mexico",
    "Argentina": "Argentina",
    "Colombia": "Colombia",
    "Brasil": "Brazil",
    "Chile": "Chile",
    "Perú": "Peru",
    "Uruguay": "Uruguay",
    "Paraguay": "Paraguay",
    "Bolivia": "Bolivia",
    "Ecuador": "Ecuador",
    "Venezuela": "Venezuela",
    "Costa Rica": "Costa Rica",
    "Panamá": "Panama",
    "Canadá": "Canada"
})

# Mapa coroplético centrado en América completa
fig_map = px.choropleth(
    map_data,
    locations="País",
    locationmode="country names",
    color="CantidadPartners",
    color_continuous_scale="blues",
    title="Cantidad de Partners por País en América",
    labels={"CantidadPartners": "Partners"},
)

fig_map.update_layout(
    geo=dict(
        projection_type="natural earth",   # proyección más natural
        scope="world",             # muestra América del Sur
        lonaxis_range=[-170, -30],         # ajusta el rango de longitud
        lataxis_range=[-60, 75],           # incluye toda América del Norte y Sur
        showframe=False,
        showcoastlines=True,
        coastlinecolor="#555",
        landcolor="#1c1c1c",
        bgcolor=BACKGROUND_COLOR
    ),
    paper_bgcolor=BACKGROUND_COLOR,
    font=dict(color=TEXT_COLOR),
    title_font=dict(size=18, color="#6cb4e4"),
)

st.plotly_chart(fig_map, use_container_width=True)


# ============================================================
# NIVEL 1B — KPIs AVANZADOS Y CORRELACIÓN DE VARIABLES
# ============================================================

st.markdown(
    "<h3 style='color:#6cb4e4;'>📊 Indicadores Avanzados y Relaciones</h3>",
    unsafe_allow_html=True
)

# ========================================
# KPI 1 — Tasa de Crecimiento Mensual (%)
# ========================================
# Tomamos las altas mensuales (ya creadas en 'evolucion')
if len(evolucion) >= 2:
    altas_mes_actual = evolucion["NuevosPartners"].iloc[-1]
    altas_mes_prev = evolucion["NuevosPartners"].iloc[-2]
    tasa_crecimiento = ((altas_mes_actual - altas_mes_prev) / altas_mes_prev) * 100 if altas_mes_prev > 0 else 0
else:
    tasa_crecimiento = 0

# ========================================
# KPI 2 — Antigüedad Promedio de Partners (meses)
# ========================================
hoy = pd.Timestamp.now()
filtered["AntiguedadMeses"] = ((hoy - filtered["FechaAlta"]).dt.days / 30).round(1)
antiguedad_prom = filtered["AntiguedadMeses"].mean().round(1)

# ========================================
# KPI 3 — País con Más Altas Recientes
# ========================================
# Consideramos el último mes disponible en 'evolucion'
if not filtered.empty:
    mes_reciente = filtered["FechaAlta"].dt.to_period("M").max()
    ultimas_altas = filtered[filtered["FechaAlta"].dt.to_period("M") == mes_reciente]
    pais_top = ultimas_altas["País"].value_counts().idxmax()
    altas_top = ultimas_altas["País"].value_counts().max()
else:
    pais_top, altas_top = "Sin datos", 0

# ========================================
# VISUALIZACIÓN DE KPIs (tarjetas)
# ========================================
col_kpiA, col_kpiB, col_kpiC = st.columns(3)

with col_kpiA:
    st.metric(
        "📈 Tasa de Crecimiento Mensual",
        f"{tasa_crecimiento:.1f}%",
        delta=f"{altas_mes_actual - altas_mes_prev:+d} altas vs mes previo"
    )

with col_kpiB:
    st.metric(
        "🕓 Antigüedad Promedio",
        f"{antiguedad_prom} meses",
        delta=None
    )

with col_kpiC:
    st.metric(
        "🌍 País con Más Altas Recientes",
        f"{pais_top} ({altas_top})",
        delta=None
    )

st.markdown("---")

# ============================================================
# GRÁFICO DE CORRELACIÓN — Antigüedad vs Notificaciones
# ============================================================

st.markdown(
    "<h4 style='color:#6cb4e4;'>🔗 Relación entre Antigüedad y Nivel de Actividad</h4>",
    unsafe_allow_html=True
)

# Mergeamos con notifications para obtener 'notification_count'
corr_df = (
    notifications
    .merge(partners, left_on="partner_id", right_on="id_partner")
    .merge(plans, left_on="plan_id", right_on="id_plan")
)

# Calculamos antigüedad y aseguramos columnas numéricas
corr_df["FechaAlta"] = pd.to_datetime(corr_df["join_date"])
corr_df["AntiguedadMeses"] = ((hoy - corr_df["FechaAlta"]).dt.days / 30).round(1)

# Creamos scatter con tendencia
fig_corr = px.scatter(
    corr_df,
    x="AntiguedadMeses",
    y="notification_count",
    color="plan_name",
    trendline="ols",
    title="Correlación entre Antigüedad del Partner y Notificaciones",
    labels={
        "AntiguedadMeses": "Antigüedad (meses)",
        "notification_count": "Cantidad de Notificaciones",
        "plan_name": "Plan"
    },
    color_discrete_sequence=COLOR_PALETTE
)

apply_dark_theme(fig_corr)
st.plotly_chart(fig_corr, use_container_width=True)



# ============================================================
# INSIGHTS FINALES
# ============================================================
st.markdown(
    "<h3 style='color:#6cb4e4;'>✅ Insights Clave</h3>",
    unsafe_allow_html=True
)
 
# -- MEJORAR ESTO !!! ---
# st.markdown(
#     """
#     <ul style="color:#E0E0E0; font-size:15px; line-height:1.5;">
#         <li>Los planes Premium y Enterprise concentran la mayor cantidad de partners activos<li>
#         <li>El crecimiento mensual muestra una tendencia positiva entre abril y septiembre<li>
#         <li>Argentina, México y Colombia lideran en cantidad de partners activos<li>
#         <li>Los planes de mayor costo presentan más notificaciones, indicando mayor compromiso<li>
#         <li>Se identifican oportunidades de expansión en países con menor representación<li>

#     </ul>
#     """,
#     unsafe_allow_html=True
# )
