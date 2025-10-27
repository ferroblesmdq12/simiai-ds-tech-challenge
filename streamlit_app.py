# # ====================================================
# # DASHBOARD - Sistema de Partners (SimiAI)
# # Descripción: Dashboard analítico para visualización
# # atravéz de "Streamlit".
# # Autor: Fernando Raúl Robles
# # Fecha: 25/10/2025
# # ====================================================

# import streamlit as st
# import pandas as pd
# import psycopg2
# import plotly.express as px

# # =============================
# # CONFIGURACIÓN INICIAL
# # =============================
# st.set_page_config(page_title="Sistema de Partners - SimiAI", layout="wide")

# # ==============================================
# # CONEXIÓN A POSTGRESQL LOCAL (no se utilizará)
# # ==============================================
# # def connect_db():
# #     try:
# #         conn = psycopg2.connect(
# #             host="localhost",
# #             database="partnersdb",
# #             user="postgres",
# #             password="ferdata",  
# #             port=5432
# #         )
# #         return conn
# #     except Exception as e:
# #         st.error(f"Error de conexión: {e}")
# #         return None

# # conn = connect_db()

# # ==============================================
# # CONEXIÓN A POSTGRESQL en la nube (neon.tech)
# # ==============================================

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
# # INTERFAZ DE USUARIO
# # =============================
# st.title("Dashboard — Sistema de Partners (SimiAI)")
# st.markdown("Visualización de métricas clave sobre partners, planes, países y actividad.")

# col1, col2, col3 = st.columns(3)

# # Paleta de colores personalizada (Blue Dashboard)
# COLOR_PALETTE = ['#354551', '#1c4c74', '#349ce4', '#6cb4e4', '#648cac', '#b2b6b0']



# # KPI 1: Partners activos por plan
# active = merged[merged["Estado"] == "Activo"]
# kpi1 = active.groupby("Plan")["Partner"].count().reset_index()
# fig1 = px.bar(kpi1, x="Plan", y="Partner", color="Plan", title="Partners Activos por Plan", color_discrete_sequence=COLOR_PALETTE)

# # KPI 2: Altas mensuales
# merged["join_month"] = pd.to_datetime(merged["join_date"]).dt.to_period("M").astype(str)
# kpi2 = merged.groupby("join_month")["Partner"].count().reset_index()
# fig2 = px.line(kpi2, x="join_month", y="Partner", title="Evolución de Altas Mensuales")


# # KPI 3: Distribución geográfica (gráfico de barras horizontales)
# kpi3 = merged.groupby("País")["Partner"].count().reset_index().sort_values("Partner", ascending=True)
# fig3 = px.bar(
#     kpi3,
#     x="Partner",
#     y="País",
#     orientation="h",
#     text="Partner",
#     color="País",
#     title="Distribución de Partners por País",
#     color_discrete_sequence=COLOR_PALETTE
# )

# fig3.update_traces(textposition="outside")
# fig3.update_layout(
#     xaxis_title="Cantidad de Partners",
#     yaxis_title="País",
#     showlegend=False,
#     plot_bgcolor="white",
#     xaxis=dict(showgrid=True, gridcolor="lightgray"),
# )

# # st.plotly_chart(fig3, use_container_width=True)

# # Mostrar KPIs en columnas

# col1.plotly_chart(fig1, use_container_width=True)
# col2.plotly_chart(fig2, use_container_width=True)
# col3.plotly_chart(fig3, use_container_width=True)

# # KPI 4: Promedio de notificaciones por plan
# notif = notifications.merge(partners, left_on="partner_id", right_on="id_partner").merge(plans, left_on="plan_id", right_on="id_plan")
# kpi4 = notif.groupby("plan_name")["notification_count"].agg(["sum", "mean"]).reset_index()
# fig4 = px.bar(kpi4, x="plan_name", y="mean", color="plan_name", title="Promedio de Notificaciones por Plan", color_discrete_sequence=COLOR_PALETTE, labels={"plan_name": "Plan", "mean": "Promedio de Notificaciones"})

# # KPI 5: Top 10 partners por notificaciones
# kpi5 = notif.groupby("partner_name")["notification_count"].sum().reset_index().sort_values("notification_count", ascending=False).head(10)
# fig5 = px.bar(kpi5, x="partner_name", y="notification_count", color="notification_count", title="Top 10 Partners por Notificaciones", color_continuous_scale=COLOR_PALETTE, labels={"partner_name": "Partner", "notification_count": "Total de Notificaciones"})

              

# st.plotly_chart(fig4, use_container_width=True)
# st.plotly_chart(fig5, use_container_width=True)

# # =============================
# # CONCLUSIÓN
# # =============================
# st.markdown("---")
# st.markdown("✅ **Interpretaciones sugeridas:**")
# st.markdown("""
# - Los planes *Standard* y *Premium*  concentran la mayor cantidad de partners activos.  
# - El crecimiento mensual muestra tendencia positiva hasta septiembre del año 2024.  
# - *Bolivia* y *Ecuador* lideran la cantidad de partners en LATAM.  
# - El promedio de notificaciones por plan confirma una mayor actividad en *Enterprise*.  
# """)

# ====================================================
# DASHBOARD - Sistema de Partners (SimiAI)
# Descripción: Dashboard analítico para visualización
# atravéz de "Streamlit".
# Autor: Fernando Raúl Robles
# Fecha: 25/10/2025
# ====================================================

#=======================================
#Segunda versión mejorada del dashboard
#=======================================

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



#===================================================
#3ra versión del dashboard - optimizada y corregida
#===================================================

# ====================================================
# DASHBOARD - Sistema de Partners (SimiAI)
# Autor: Fernando Raúl Robles
# Fecha: 26/10/2025
# ====================================================

import streamlit as st
import pandas as pd
import psycopg2
import plotly.express as px

# =============================
# CONFIGURACIÓN INICIAL
# =============================
st.set_page_config(page_title="Sistema de Partners - SimiAI", layout="wide")

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
# MERGE DE DATOS
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

merged["join_date"] = pd.to_datetime(merged["join_date"])

# =============================
# PALETA DE COLORES
# =============================
COLOR_PALETTE = ['#354551', '#1c4c74', '#349ce4', '#6cb4e4', '#648cac', '#b2b6b0']
CHART_BG = "#F4F7FB"  # gris azulado suave para fondo uniforme

# =============================
# FILTROS INTERACTIVOS
# =============================
st.sidebar.header("🎚️ Filtros de Análisis")

pais_sel = st.sidebar.multiselect(
    "🌎 Seleccionar País:",
    options=merged["País"].unique(),
    default=list(merged["País"].unique())
)

plan_sel = st.sidebar.multiselect(
    "📦 Seleccionar Plan Comercial:",
    options=merged["Plan"].unique(),
    default=list(merged["Plan"].unique())
)

fecha_min = merged["join_date"].min()
fecha_max = merged["join_date"].max()

fecha_sel = st.sidebar.date_input(
    "📅 Rango de Fechas de Alta:",
    value=(fecha_min, fecha_max),
    min_value=fecha_min,
    max_value=fecha_max
)

# Filtrado dinámico
merged_filtered = merged[
    (merged["País"].isin(pais_sel)) &
    (merged["Plan"].isin(plan_sel)) &
    (merged["join_date"].between(fecha_sel[0], fecha_sel[1]))
]

# =============================
# KPI RESUMEN (Tarjetas)
# =============================
total_partners = len(merged_filtered)
active_partners = len(merged_filtered[merged_filtered["Estado"] == "Activo"])
inactive_partners = len(merged_filtered[merged_filtered["Estado"] != "Activo"])
avg_notifications = notifications["notification_count"].mean().round(2)

col_a, col_b, col_c, col_d = st.columns(4)
with col_a: st.metric("🌍 Total de Partners", f"{total_partners}")
with col_b: st.metric("✅ Partners Activos", f"{active_partners}")
with col_c: st.metric("🧩 Partners Inactivos", f"{inactive_partners}")
with col_d: st.metric("📨 Promedio Notificaciones", f"{avg_notifications}")

# =============================
# KPI: Partners Activos vs Inactivos
# =============================
status_counts = merged_filtered["Estado"].value_counts().reset_index()
status_counts.columns = ["Estado", "Cantidad"]

fig_status = px.pie(
    status_counts,
    names="Estado",
    values="Cantidad",
    title="Distribución de Partners Activos vs No Activos (%)",
    color_discrete_sequence=COLOR_PALETTE
)
fig_status.update_layout(
    paper_bgcolor=CHART_BG,
    plot_bgcolor=CHART_BG,
    title_font=dict(size=18, color="#1c4c74"),
    font=dict(color="#354551")
)
st.plotly_chart(fig_status, use_container_width=True, key="status")

# =============================
# KPI: Partners Activos por Plan
# =============================
col1, col2, col3 = st.columns(3)

active = merged_filtered[merged_filtered["Estado"] == "Activo"]
kpi1 = active.groupby("Plan")["Partner"].count().reset_index()
fig1 = px.bar(
    kpi1, x="Plan", y="Partner", color="Plan",
    title="Partners Activos por Plan",
    color_discrete_sequence=COLOR_PALETTE,
    labels={"Plan": "Plan Comercial", "Partner": "Cantidad de Partners"}
)
fig1.update_layout(paper_bgcolor=CHART_BG, plot_bgcolor=CHART_BG)
col1.plotly_chart(fig1, use_container_width=True, key="fig1")

# =============================
# KPI: Evolución de Altas Mensuales
# =============================
merged_filtered["join_month"] = merged_filtered["join_date"].dt.to_period("M").astype(str)
kpi2 = merged_filtered.groupby("join_month")["Partner"].count().reset_index()
fig2 = px.line(
    kpi2, x="join_month", y="Partner",
    title="Evolución de Altas Mensuales",
    markers=True,
    labels={"join_month": "Mes de Alta", "Partner": "Nuevos Partners"}
)
fig2.update_traces(line_color="#349ce4", marker_color="#1c4c74")
fig2.update_layout(paper_bgcolor=CHART_BG, plot_bgcolor=CHART_BG)
col2.plotly_chart(fig2, use_container_width=True, key="fig2")

# =============================
# KPI: Distribución Geográfica
# =============================
kpi3 = merged_filtered.groupby("País")["Partner"].count().reset_index().sort_values("Partner", ascending=True)
fig3 = px.bar(
    kpi3, x="Partner", y="País",
    orientation="h", text="Partner", color="País",
    title="Distribución de Partners por País",
    color_discrete_sequence=COLOR_PALETTE,
    labels={"País": "País", "Partner": "Cantidad"}
)
fig3.update_traces(textposition="outside")
fig3.update_layout(paper_bgcolor=CHART_BG, plot_bgcolor=CHART_BG, showlegend=False)
col3.plotly_chart(fig3, use_container_width=True, key="fig3")

# =============================
# KPI: Promedio de Notificaciones por Plan
# =============================
notif = notifications.merge(partners, left_on="partner_id", right_on="id_partner").merge(plans, left_on="plan_id", right_on="id_plan")
kpi4 = notif.groupby("plan_name")["notification_count"].agg(["sum", "mean"]).reset_index()
fig4 = px.bar(
    kpi4, x="plan_name", y="mean",
    color="plan_name", title="Promedio de Notificaciones por Plan",
    color_discrete_sequence=COLOR_PALETTE,
    labels={"plan_name": "Plan Comercial", "mean": "Promedio de Notificaciones"}
)
fig4.update_layout(paper_bgcolor=CHART_BG, plot_bgcolor=CHART_BG, showlegend=False)
st.plotly_chart(fig4, use_container_width=True, key="fig4")

# =============================
# KPI: Top 10 Partners por Notificaciones
# =============================
kpi5 = notif.groupby("partner_name")["notification_count"].sum().reset_index().sort_values("notification_count", ascending=False).head(10)
fig5 = px.bar(
    kpi5, x="partner_name", y="notification_count",
    color="notification_count", title="Top 10 Partners por Notificaciones",
    color_continuous_scale=COLOR_PALETTE,
    labels={"partner_name": "Partner", "notification_count": "Total de Notificaciones"}
)
fig5.update_layout(paper_bgcolor=CHART_BG, plot_bgcolor=CHART_BG)
st.plotly_chart(fig5, use_container_width=True, key="fig5")

# =============================
# CONCLUSIONES
# =============================
st.markdown("---")
st.markdown("✅ **Insights Clave:**")
st.markdown("""
- Los planes *Standard* y *Premium* concentran la mayor cantidad de partners activos.  
- El crecimiento mensual muestra tendencia positiva hasta septiembre de 2024.  
- *Bolivia* y *Ecuador* lideran la red de partners en LATAM.  
- Los planes *Enterprise* tienen un promedio más alto de notificaciones enviadas.  
""")
