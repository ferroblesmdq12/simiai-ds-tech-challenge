# # # ====================================================
# # # DASHBOARD - Sistema de Partners (SimiAI)
# # # Descripción: Dashboard analítico para visualización
# # # a través de "Streamlit".
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

# (1) Intentamos abrir conexión para chequeo (opcional, la carga real la hace load_data)
conn = None
try:
    conn = init_connection()
    with conn.cursor() as cur:
        cur.execute("SELECT NOW();")
        result = cur.fetchone()
    st.sidebar.success(f"🟢 Conectado a Neon.tech ({result[0]})")
except Exception as e:
    st.sidebar.warning(f"⚠️ No se pudo verificar NOW(): {e}")

# (2) Carga de dataframes desde el loader (única vez)
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

merged["FechaAlta"] = pd.to_datetime(merged["FechaAlta"], errors="coerce")

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

paises_unicos = sorted([p for p in merged["País"].dropna().unique().tolist()])
opcion_pais = st.sidebar.selectbox(" País", ["Todos"] + paises_unicos, index=0)

planes_unicos = sorted([p for p in merged["Plan"].dropna().unique().tolist()])
opcion_plan = st.sidebar.selectbox(" Plan Comercial", ["Todos"] + planes_unicos, index=0)

fecha_min = merged["FechaAlta"].min() if not merged.empty else pd.Timestamp.today() - pd.Timedelta(days=365)
fecha_max = merged["FechaAlta"].max() if not merged.empty else pd.Timestamp.today()

rango_fecha = st.sidebar.date_input(
    " Rango de Fecha de Alta",
    value=(fecha_min, fecha_max),
    min_value=fecha_min,
    max_value=fecha_max
)
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

# Notificaciones filtradas: respetan país/plan y sólo de partners filtrados
notif_full = (
    notifications
    .merge(partners,  left_on="partner_id", right_on="id_partner", how="left")   # aporta partner_name, country_id, plan_id, industry, etc.
    .merge(plans,     left_on="plan_id",    right_on="id_plan",    how="left")   # aporta plan_name
    .merge(countries, left_on="country_id", right_on="id_country", how="left")   # aporta country_name
)

# Filtramos por país/plan explícitos
if opcion_pais != "Todos":
    notif_full = notif_full[notif_full["country_name"] == opcion_pais]
if opcion_plan != "Todos":
    notif_full = notif_full[notif_full["plan_name"] == opcion_plan]

# Filtramos para que sólo queden notificaciones de los partners visibles
if not filtered.empty and "id_partner" in filtered.columns:
    notif_full = notif_full[notif_full["id_partner"].isin(filtered["id_partner"].unique())]

# =============================
# HEADER (título)
# =============================
st.markdown(
    """
    <h1 style="color:#E0E0E0; margin-bottom:0;"> SimiAI - Sistema de Partners </h1>
    <p style="color:#b2b6b0; margin-top:4px;">
    Vista ejecutiva y operativa de la red de partners. <br/>
    Los filtros de la izquierda impactan en todas las métrricas, incluidas las operativas de notificaciones.
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
        setTimeout(() => {
            const now = new Date();
            const options = {
                year: 'numeric', month: '2-digit', day: '2-digit',
                hour: '2-digit', minute: '2-digit', second: '2-digit'
            };
            const localTime = now.toLocaleString([], options);
            document.getElementById("update-time").innerHTML =
                "📅 Datos actualizados al " + localTime;
        }, 1200);
    </script>
    """,
    height=40
)

# ============================================================
# NIVEL 1 — VISIÓN GENERAL (tarjetas KPI)
# ============================================================
total_partners      = int(len(filtered))
activos_partners    = int(len(filtered[filtered["Estado"] == "Activo"])) if not filtered.empty else 0
inactivos_partners  = total_partners - activos_partners
prom_notif_global   = float(notif_full["notification_count"].mean().round(2)) if not notif_full.empty else 0.0

col_kpi1, col_kpi2, col_kpi3, col_kpi4 = st.columns(4)
col_kpi1.metric(" Total de Partners", total_partners)
col_kpi2.metric(" Partners Activos", activos_partners)
col_kpi3.metric(" Partners No Activos", inactivos_partners)
col_kpi4.metric(" Promedio Notificaciones", prom_notif_global)

st.markdown("---")


# ============================================================
# NIVEL 2 — DISTRIBUCIÓN ALTA NIVEL
#    - Estado (Activos vs No Activos)
#    - Distribución geográfica
# ============================================================
col_dist1, col_dist2 = st.columns(2)

# 2A. Estado (pie activos vs no activos)
if not filtered.empty:
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
else:
    col_dist1.info("Sin datos para la distribución de estado en el rango/filtros seleccionados.")

# 2B. Distribución geográfica (barras horizontales)
if not filtered.empty:
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
else:
    col_dist2.info("Sin datos para la distribución geográfica en el rango/filtros seleccionados.")

st.markdown("---")

# ============================================================
# NIVEL 3 — EVOLUCIÓN TEMPORAL / TENDENCIA (Altas mensuales)
# ============================================================
if not filtered.empty:
    # usamos 'evolucion' ya calculado
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
else:
    st.info("Sin datos para la evolución temporal con los filtros actuales.")

st.markdown("---")

# ============================================================
# NIVEL 4 — ANÁLISIS POR PLAN Y TOP PARTNERS
# ============================================================
col_plan, col_top = st.columns(2)

# 4A. Partners activos por plan (solo filtrados)
if not filtered.empty:
    activos_filtrados = filtered[filtered["Estado"] == "Activo"]
    if not activos_filtrados.empty:
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
    else:
        col_plan.info("No hay partners activos con los filtros actuales.")
else:
    col_plan.info("Sin datos con los filtros seleccionados.")

# 4B. Top 10 partners por notificaciones (filtrado)
if not notif_full.empty:
    top_notif = (
        notif_full
        .groupby(["id_partner", "partner_name"])["notification_count"]
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
        color_continuous_scale="Blues",
        labels={"partner_name": "Partner", "notification_count": "Total Notificaciones"}
    )
    apply_dark_theme(fig_top)
    col_top.plotly_chart(fig_top, use_container_width=True)
else:
    col_top.info("Sin notificaciones para los filtros actuales.")

st.markdown("---")

# ============================================================
# NIVEL 5 — DISTRIBUCIÓN DE PARTNERS POR INDUSTRIA
# ============================================================
st.markdown("<h3 style='color:#6cb4e4;'>🏭 Distribución de Partners por Industria</h3>", unsafe_allow_html=True)

if not filtered.empty and "industry" in filtered.columns:
    industria_counts = (
        filtered
        .groupby("industry")["id_partner"]
        .count()
        .reset_index()
        .rename(columns={"industry": "Industria", "id_partner": "Cantidad"})
        .sort_values("Cantidad", ascending=False)
    )
    if not industria_counts.empty:
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
    else:
        st.info("No hay datos de industria para los filtros vigentes.")
else:
    st.info("La columna de industria no está disponible o no hay datos filtrados.")

# ============================================================
# NIVEL 6 — MAPA GEOGRÁFICO DE PARTNERS EN AMÉRICA
# ============================================================
st.markdown("<h3 style='color:#6cb4e4;'>🌎 Distribución Geográfica de Partners en América</h3>", unsafe_allow_html=True)

if not filtered.empty:
    map_data = (
        filtered.groupby("País")["Partner"]
        .count()
        .reset_index()
        .rename(columns={"Partner": "CantidadPartners"})
    )

    # Normalización de nombres (si tu dataset viene en español o mixto)
    map_data["País"] = map_data["País"].replace({
        "Estados Unidos": "United States",
        "USA": "United States",
        "México": "Mexico",
        "Brasil": "Brazil",
        "Perú": "Peru",
        "Panamá": "Panama",
        "Canadá": "Canada",
    })

    fig_map = px.choropleth(
        map_data,
        locations="País",
        locationmode="country names",
        color="CantidadPartners",
        color_continuous_scale="Blues",
        title="Cantidad de Partners por País (Américas)",
        labels={"CantidadPartners": "Partners"},
    )

    fig_map.update_layout(
        geo=dict(
            projection_type="natural earth",
            scope="world",               # usamos 'world' y acotamos por rangos para cubrir ambas Américas
            lonaxis_range=[-170, -30],   # longitudes que abarcan América
            lataxis_range=[-60, 75],     # latitudes de extremo sur a norte
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
else:
    st.info("Sin datos para el mapa con los filtros actuales.")

# ============================================================
# NIVEL 1B — KPIs AVANZADOS Y CORRELACIÓN DE VARIABLES
# ============================================================
st.markdown("<h3 style='color:#6cb4e4;'>📊 Indicadores Avanzados y Relaciones</h3>", unsafe_allow_html=True)

# Serie mensual para crecimiento (según filtro)
if not filtered.empty:
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

# KPI 1 — Tasa de Crecimiento Mensual
if len(evolucion) >= 2:
    altas_mes_actual = int(evolucion["NuevosPartners"].iloc[-1])
    altas_mes_prev   = int(evolucion["NuevosPartners"].iloc[-2])
    tasa_crecimiento = ( (altas_mes_actual - altas_mes_prev) / altas_mes_prev * 100 ) if altas_mes_prev > 0 else 0.0
else:
    altas_mes_actual, altas_mes_prev, tasa_crecimiento = 0, 0, 0.0

# KPI 2 — Antigüedad Promedio (meses)
hoy = pd.Timestamp.now()
if not filtered.empty:
    filtered["AntiguedadMeses"] = ((hoy - filtered["FechaAlta"]).dt.days / 30).round(1)
    antiguedad_prom = float(filtered["AntiguedadMeses"].mean().round(1))
else:
    antiguedad_prom = 0.0

# KPI 3 — País con Más Altas Recientes
if not filtered.empty:
    mes_reciente = filtered["FechaAlta"].dt.to_period("M").max()
    ultimas_altas = filtered[filtered["FechaAlta"].dt.to_period("M") == mes_reciente]
    if not ultimas_altas.empty:
        pais_top = str(ultimas_altas["País"].value_counts().idxmax())
        altas_top = int(ultimas_altas["País"].value_counts().max())
    else:
        pais_top, altas_top = "Sin datos", 0
else:
    pais_top, altas_top = "Sin datos", 0

# Tarjetas KPI avanzados
col_kpiA, col_kpiB, col_kpiC = st.columns(3)
col_kpiA.metric("📈 Crecimiento Mensual", f"{tasa_crecimiento:.1f}%", delta=f"{altas_mes_actual - altas_mes_prev:+d}")
col_kpiB.metric("🕓 Antigüedad Promedio", f"{antiguedad_prom:.1f} meses")
col_kpiC.metric("🌍 País con Más Altas", f"{pais_top} ({altas_top})")

st.markdown("---")

# ============================================================
# GRÁFICO DE CORRELACIÓN — Antigüedad vs Notificaciones
# ============================================================
st.markdown("<h4 style='color:#6cb4e4;'>🔗 Relación entre Antigüedad y Nivel de Actividad</h4>", unsafe_allow_html=True)

# Vinculamos notificaciones con el subconjunto filtrado (por partner visible)
corr_df = pd.DataFrame()
if not notif_full.empty and not filtered.empty:
    corr_df = (
        notif_full
        .merge(
            filtered[["id_partner", "Partner", "FechaAlta", "Plan", "País"]],
            left_on="id_partner", right_on="id_partner", how="inner"
        )
    )
if not corr_df.empty:
    corr_df["AntiguedadMeses"] = ((hoy - corr_df["FechaAlta"]).dt.days / 30).round(1)
    # Trendline puede requerir statsmodels; lo hacemos robusto
    try:
        fig_corr = px.scatter(
            corr_df,
            x="AntiguedadMeses",
            y="notification_count",
            color="Plan",
            trendline="ols",
            title="Correlación entre Antigüedad del Partner y Notificaciones",
            labels={"AntiguedadMeses": "Antigüedad (meses)", "notification_count": "Notificaciones"},
            color_discrete_sequence=COLOR_PALETTE
        )
    except Exception:
        fig_corr = px.scatter(
            corr_df,
            x="AntiguedadMeses",
            y="notification_count",
            color="Plan",
            title="Correlación entre Antigüedad del Partner y Notificaciones",
            labels={"AntiguedadMeses": "Antigüedad (meses)", "notification_count": "Notificaciones"},
            color_discrete_sequence=COLOR_PALETTE
        )
    apply_dark_theme(fig_corr)
    st.plotly_chart(fig_corr, use_container_width=True)
else:
    st.info("⚠️ No hay datos suficientes para mostrar correlación con los filtros aplicados.")

st.markdown("---")


# ============================================================
# INSIGHTS FINALES
# ============================================================
st.markdown("<h3 style='color:#6cb4e4;'>✅ Insights Clave</h3>", unsafe_allow_html=True)
# Podés completar con st.markdown bullets dinámicos según KPIs calculados.
