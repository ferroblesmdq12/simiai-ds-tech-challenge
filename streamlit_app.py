# # # ====================================================
# # # DASHBOARD - Sistema de Partners (SimiAI)
# # # Descripción: Dashboard analítico para visualización
# # # atravéz de "Streamlit".
# # # Autor: Fernando Raúl Robles
# # # Fecha: 25/10/2025
# # # ====================================================

# # import streamlit as st
# # import pandas as pd
# # import psycopg2
# # import plotly.express as px

# # # =============================
# # # CONFIGURACIÓN INICIAL
# # # =============================
# # st.set_page_config(page_title="Sistema de Partners - SimiAI", layout="wide")

# # # ==============================================
# # # CONEXIÓN A POSTGRESQL LOCAL (no se utilizará)
# # # ==============================================
# # # def connect_db():
# # #     try:
# # #         conn = psycopg2.connect(
# # #             host="localhost",
# # #             database="partnersdb",
# # #             user="postgres",
# # #             password="ferdata",  
# # #             port=5432
# # #         )
# # #         return conn
# # #     except Exception as e:
# # #         st.error(f"Error de conexión: {e}")
# # #         return None

# # # conn = connect_db()

# # # ==============================================
# # # CONEXIÓN A POSTGRESQL en la nube (neon.tech)
# # # ==============================================

# # def connect_db():
# #     try:
# #         conn = psycopg2.connect(
# #             host="ep-red-feather-aca9j4sc-pooler.sa-east-1.aws.neon.tech",
# #             database="partnersdb",
# #             user="neondb_owner",
# #             password="npg_U7EYlIQ6XZPO",
# #             port="5432",
# #             sslmode="require"
# #         )
# #         return conn
# #     except Exception as e:
# #         st.error(f"Error de conexión: {e}")
# #         return None
# # conn = connect_db()

# # # =============================
# # # CARGA DE DATOS
# # # =============================
# # @st.cache_data
# # def load_data():
# #     partners = pd.read_sql("SELECT * FROM partners;", conn)
# #     countries = pd.read_sql("SELECT * FROM countries;", conn)
# #     plans = pd.read_sql("SELECT * FROM plans;", conn)
# #     statuses = pd.read_sql("SELECT * FROM statuses;", conn)
# #     notifications = pd.read_sql("SELECT * FROM notifications;", conn)
# #     return partners, countries, plans, statuses, notifications

# # partners, countries, plans, statuses, notifications = load_data()

# # # =============================
# # # MERGE DE DATOS PARA ANÁLISIS
# # # =============================
# # merged = (
# #     partners
# #     .merge(countries, left_on="country_id", right_on="id_country")
# #     .merge(plans, left_on="plan_id", right_on="id_plan")
# #     .merge(statuses, left_on="status_id", right_on="id_status")
# # )

# # merged.rename(columns={
# #     "country_name": "País",
# #     "plan_name": "Plan",
# #     "status_name": "Estado",
# #     "partner_name": "Partner"
# # }, inplace=True)

# # # =============================
# # # INTERFAZ DE USUARIO
# # # =============================
# # st.title("Dashboard — Sistema de Partners (SimiAI)")
# # st.markdown("Visualización de métricas clave sobre partners, planes, países y actividad.")

# # col1, col2, col3 = st.columns(3)

# # # Paleta de colores personalizada (Blue Dashboard)
# # COLOR_PALETTE = ['#354551', '#1c4c74', '#349ce4', '#6cb4e4', '#648cac', '#b2b6b0']



# # # KPI 1: Partners activos por plan
# # active = merged[merged["Estado"] == "Activo"]
# # kpi1 = active.groupby("Plan")["Partner"].count().reset_index()
# # fig1 = px.bar(kpi1, x="Plan", y="Partner", color="Plan", title="Partners Activos por Plan", color_discrete_sequence=COLOR_PALETTE)

# # # KPI 2: Altas mensuales
# # merged["join_month"] = pd.to_datetime(merged["join_date"]).dt.to_period("M").astype(str)
# # kpi2 = merged.groupby("join_month")["Partner"].count().reset_index()
# # fig2 = px.line(kpi2, x="join_month", y="Partner", title="Evolución de Altas Mensuales")


# # # KPI 3: Distribución geográfica (gráfico de barras horizontales)
# # kpi3 = merged.groupby("País")["Partner"].count().reset_index().sort_values("Partner", ascending=True)
# # fig3 = px.bar(
# #     kpi3,
# #     x="Partner",
# #     y="País",
# #     orientation="h",
# #     text="Partner",
# #     color="País",
# #     title="Distribución de Partners por País",
# #     color_discrete_sequence=COLOR_PALETTE
# # )

# # fig3.update_traces(textposition="outside")
# # fig3.update_layout(
# #     xaxis_title="Cantidad de Partners",
# #     yaxis_title="País",
# #     showlegend=False,
# #     plot_bgcolor="white",
# #     xaxis=dict(showgrid=True, gridcolor="lightgray"),
# # )

# # # st.plotly_chart(fig3, use_container_width=True)

# # # Mostrar KPIs en columnas

# # col1.plotly_chart(fig1, use_container_width=True)
# # col2.plotly_chart(fig2, use_container_width=True)
# # col3.plotly_chart(fig3, use_container_width=True)

# # # KPI 4: Promedio de notificaciones por plan
# # notif = notifications.merge(partners, left_on="partner_id", right_on="id_partner").merge(plans, left_on="plan_id", right_on="id_plan")
# # kpi4 = notif.groupby("plan_name")["notification_count"].agg(["sum", "mean"]).reset_index()
# # fig4 = px.bar(kpi4, x="plan_name", y="mean", color="plan_name", title="Promedio de Notificaciones por Plan", color_discrete_sequence=COLOR_PALETTE, labels={"plan_name": "Plan", "mean": "Promedio de Notificaciones"})

# # # KPI 5: Top 10 partners por notificaciones
# # kpi5 = notif.groupby("partner_name")["notification_count"].sum().reset_index().sort_values("notification_count", ascending=False).head(10)
# # fig5 = px.bar(kpi5, x="partner_name", y="notification_count", color="notification_count", title="Top 10 Partners por Notificaciones", color_continuous_scale=COLOR_PALETTE, labels={"partner_name": "Partner", "notification_count": "Total de Notificaciones"})

              

# # st.plotly_chart(fig4, use_container_width=True)
# # st.plotly_chart(fig5, use_container_width=True)

# # # =============================
# # # CONCLUSIÓN
# # # =============================
# # st.markdown("---")
# # st.markdown("✅ **Interpretaciones sugeridas:**")
# # st.markdown("""
# # - Los planes *Standard* y *Premium*  concentran la mayor cantidad de partners activos.  
# # - El crecimiento mensual muestra tendencia positiva hasta septiembre del año 2024.  
# # - *Bolivia* y *Ecuador* lideran la cantidad de partners en LATAM.  
# # - El promedio de notificaciones por plan confirma una mayor actividad en *Enterprise*.  
# # """)

# # ====================================================
# # DASHBOARD - Sistema de Partners (SimiAI)
# # Descripción: Dashboard analítico para visualización
# # atravéz de "Streamlit".
# # Autor: Fernando Raúl Robles
# # Fecha: 25/10/2025
# # ====================================================

# #=======================================
# #Segunda versión mejorada del dashboard
# #=======================================

# import streamlit as st
# import pandas as pd
# import psycopg2
# import plotly.express as px

# # =============================
# # CONFIGURACIÓN INICIAL
# # =============================
# st.set_page_config(page_title="Sistema de Partners - SimiAI", layout="wide")

# # =============================
# # CONEXIÓN A POSTGRESQL en la nube (neon.tech)
# # =============================
# def connect_db():
#     try:
#         conn = psycopg2.connect(
#             host="ep-red-feather-aca9j4sc-pooler.sa-east-1.aws.neon.tech",
#             database="partnersdb",
#             user="neondb_owner",
#             password="npg_U7EYlIQ6XZPO",
#             port="5432",
#             sslmode="require"
#         )
#         return conn
#     except Exception as e:
#         st.error(f"Error de conexión: {e}")
#         return None

# conn = connect_db()

# # =============================
# # CARGA DE DATOS
# # =============================
# @st.cache_data
# def load_data():
#     partners = pd.read_sql("SELECT * FROM partners;", conn)
#     countries = pd.read_sql("SELECT * FROM countries;", conn)
#     plans = pd.read_sql("SELECT * FROM plans;", conn)
#     statuses = pd.read_sql("SELECT * FROM statuses;", conn)
#     notifications = pd.read_sql("SELECT * FROM notifications;", conn)
#     return partners, countries, plans, statuses, notifications

# partners, countries, plans, statuses, notifications = load_data()

# # =============================
# # MERGE DE DATOS PARA ANÁLISIS
# # =============================
# merged = (
#     partners
#     .merge(countries, left_on="country_id", right_on="id_country")
#     .merge(plans, left_on="plan_id", right_on="id_plan")
#     .merge(statuses, left_on="status_id", right_on="id_status")
# )

# merged.rename(columns={
#     "country_name": "País",
#     "plan_name": "Plan",
#     "status_name": "Estado",
#     "partner_name": "Partner"
# }, inplace=True)

# # =============================
# # PALETA DE COLORES
# # =============================
# COLOR_PALETTE = ['#354551', '#1c4c74', '#349ce4', '#6cb4e4', '#648cac', '#b2b6b0']

# # =============================
# # INTERFAZ DE USUARIO
# # =============================
# st.title("📊 Dashboard — Sistema de Partners (SimiAI)")
# st.markdown("Visualización jerárquica de métricas clave sobre partners, planes, países y actividad.")

# # =============================
# # NIVEL 1: KPI RESUMEN (tarjetas)
# # =============================
# total_partners = len(partners)
# active_partners = len(merged[merged["Estado"] == "Activo"])
# inactive_partners = len(merged[merged["Estado"] != "Activo"])
# avg_notifications = notifications["notification_count"].mean().round(2)

# col_a, col_b, col_c, col_d = st.columns(4)
# with col_a: st.metric("🌍 Total de Partners", f"{total_partners}")
# with col_b: st.metric("✅ Partners Activos", f"{active_partners}")
# with col_c: st.metric("🧩 Partners Inactivos", f"{inactive_partners}")
# with col_d: st.metric("📨 Promedio Notificaciones", f"{avg_notifications}")

# # =============================
# # NIVEL 2: DISTRIBUCIÓN GENERAL
# # =============================
# status_counts = merged["Estado"].value_counts().reset_index()
# status_counts.columns = ["Estado", "Cantidad"]
# status_counts["Porcentaje"] = (status_counts["Cantidad"] / status_counts["Cantidad"].sum() * 100).round(2)

# fig_status = px.pie(
#     status_counts,
#     names="Estado",
#     values="Cantidad",
#     title="Distribución de Partners Activos vs No Activos (%)",
#     color_discrete_sequence=COLOR_PALETTE
# )
# fig_status.update_traces(textinfo="percent+label", pull=[0.05, 0.05], textfont_size=14)
# fig_status.update_layout(
#     title_font=dict(size=18, color="#1c4c74"),
#     font=dict(color="#354551"),
#     paper_bgcolor="white",
#     plot_bgcolor="white"
# )
# st.plotly_chart(fig_status, use_container_width=True, key="fig_status")

# # =============================
# # NIVEL 3: KPIs DE NEGOCIO
# # =============================
# col1, col2, col3 = st.columns(3)

# # KPI 1: Partners activos por plan
# active = merged[merged["Estado"] == "Activo"]
# kpi1 = active.groupby("Plan")["Partner"].count().reset_index()
# fig1 = px.bar(
#     kpi1,
#     x="Plan",
#     y="Partner",
#     color="Plan",
#     title="Partners Activos por Plan",
#     color_discrete_sequence=COLOR_PALETTE,
#     labels={"Plan": "Plan Comercial", "Partner": "Cantidad de Partners"}
# )
# fig1.update_layout(plot_bgcolor="white")
# col1.plotly_chart(fig1, use_container_width=True, key="fig1")

# # KPI 2: Altas mensuales
# merged["join_month"] = pd.to_datetime(merged["join_date"]).dt.to_period("M").astype(str)
# kpi2 = merged.groupby("join_month")["Partner"].count().reset_index()
# fig2 = px.line(
#     kpi2,
#     x="join_month",
#     y="Partner",
#     title="Evolución de Altas Mensuales",
#     labels={"join_month": "Mes de Alta", "Partner": "Cantidad de Nuevos Partners"},
#     markers=True
# )
# fig2.update_traces(line_color="#1c4c74", marker_color="#349ce4")
# col2.plotly_chart(fig2, use_container_width=True, key="fig2")

# # KPI 3: Distribución geográfica
# kpi3 = merged.groupby("País")["Partner"].count().reset_index().sort_values("Partner", ascending=True)
# fig3 = px.bar(
#     kpi3,
#     x="Partner",
#     y="País",
#     orientation="h",
#     text="Partner",
#     color="País",
#     title="Distribución de Partners por País",
#     color_discrete_sequence=COLOR_PALETTE,
#     labels={"País": "País", "Partner": "Cantidad de Partners"}
# )
# fig3.update_traces(textposition="outside")
# fig3.update_layout(plot_bgcolor="white", showlegend=False)
# col3.plotly_chart(fig3, use_container_width=True, key="fig3")

# # =============================
# # NIVEL 4: ANÁLISIS OPERATIVO
# # =============================
# notif = notifications.merge(partners, left_on="partner_id", right_on="id_partner").merge(plans, left_on="plan_id", right_on="id_plan")

# # KPI 4: Promedio de notificaciones por plan
# kpi4 = notif.groupby("plan_name")["notification_count"].agg(["sum", "mean"]).reset_index()
# kpi4["mean"] = kpi4["mean"].round(2)
# fig4 = px.bar(
#     kpi4,
#     x="plan_name",
#     y="mean",
#     color="plan_name",
#     title="Promedio de Notificaciones por Plan",
#     color_discrete_sequence=COLOR_PALETTE,
#     labels={"plan_name": "Plan Comercial", "mean": "Promedio de Notificaciones"}
# )
# fig4.update_layout(plot_bgcolor="white", showlegend=False)
# st.plotly_chart(fig4, use_container_width=True, key="fig4")

# # KPI 5: Top 10 partners por notificaciones
# kpi5 = notif.groupby("partner_name")["notification_count"].sum().reset_index().sort_values("notification_count", ascending=False).head(10)
# fig5 = px.bar(
#     kpi5,
#     x="partner_name",
#     y="notification_count",
#     color="notification_count",
#     title="Top 10 Partners por Notificaciones",
#     color_continuous_scale=COLOR_PALETTE,
#     labels={"partner_name": "Partner", "notification_count": "Total de Notificaciones"}
# )
# fig5.update_layout(plot_bgcolor="white")
# st.plotly_chart(fig5, use_container_width=True, key="fig5")

# # =============================
# # CONCLUSIONES
# # =============================
# st.markdown("---")
# st.markdown("✅ **Insights Clave:**")
# st.markdown("""
# - Los planes *Standard* y *Premium* concentran la mayor cantidad de partners activos.  
# - El crecimiento mensual muestra tendencia positiva hasta septiembre de 2024.  
# - *Bolivia* y *Ecuador* lideran la red de partners en LATAM.  
# - Los planes *Enterprise* tienen un promedio más alto de notificaciones enviadas.  
# """)


#=======================================
#tercera versión mejorada del dashboard
#=======================================

# ====================================================
# DASHBOARD - Sistema de Partners (SimiAI)
# Autor: Fernando Raúl Robles
# Versión: 27/10/2025
# ====================================================

import streamlit as st
import pandas as pd
import psycopg2
import plotly.express as px
import datetime

# =============================
# CONFIG INICIAL
# =============================
st.set_page_config(
    page_title="Sistema de Partners - SimiAI",
    layout="wide"
)

# =============================
# CONEXIÓN A POSTGRESQL (Neon.tech)
# =============================
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
st.sidebar.header("🎚 Filtros")

# Filtro País
paises_unicos = sorted(merged["País"].unique().tolist())
opcion_pais = st.sidebar.selectbox(
    "🌎 País",
    options=["Todos"] + paises_unicos,
    index=0
)

# Filtro Plan
planes_unicos = sorted(merged["Plan"].unique().tolist())
opcion_plan = st.sidebar.selectbox(
    "📦 Plan Comercial",
    options=["Todos"] + planes_unicos,
    index=0
)

# Filtro Rango de Fechas
fecha_min = merged["FechaAlta"].min()
fecha_max = merged["FechaAlta"].max()

rango_fecha = st.sidebar.date_input(
    "📅 Rango de Fecha de Alta",
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
    <h1 style="color:#E0E0E0; margin-bottom:0;">📊 Dashboard — Sistema de Partners (SimiAI)</h1>
    <p style="color:#b2b6b0; margin-top:4px;">
    Vista ejecutiva y operativa de la red de partners. <br/>
    Los filtros de la izquierda impactan en todas las métricas excepto las operativas globales de notificaciones.
    </p>
    """,
    unsafe_allow_html=True
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
    st.metric("🌍 Total de Partners", total_partners)

with col_kpi2:
    st.metric("✅ Partners Activos", activos_partners)

with col_kpi3:
    st.metric("🧩 Partners No Activos", inactivos_partners)

with col_kpi4:
    st.metric("📨 Promedio Notificaciones (global)", prom_notif_global)

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
        <li>Los planes con más partners activos representan las líneas comerciales con mejor adopción.</li>
        <li>El ritmo de altas mensuales permite monitorear la capacidad de adquisición de nuevos partners.</li>
        <li>Los países con mayor presencia deberían priorizarse para soporte comercial y retención.</li>
        <li>Los partners con más notificaciones muestran una mayor actividad operativa y engagement en la plataforma.</li>
    </ul>
    """,
    unsafe_allow_html=True
)
