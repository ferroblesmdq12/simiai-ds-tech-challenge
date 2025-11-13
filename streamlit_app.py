# # # # ====================================================
# # # # DASHBOARD - Sistema de Partners (SimiAI)
# # # # Descripción: Dashboard analítico para visualización
# # # # atravéz de "Streamlit".
# # # # Autor: Fernando Raúl Robles
# # # # Fecha: 27/10/2025
# # # # ====================================================

# # =============================
# # IMPORTS PRINCIPALES
# # =============================

# import streamlit as st
# import pandas as pd
# import psycopg2
# import plotly.express as px
# import datetime
# import traceback

# # Importamos los módulos personalizados
# from src.db_connection import init_connection
# from src.data_loader import load_data


# # =============================
# # CONFIG INICIAL
# # =============================
# st.set_page_config(
#     page_title="Sistema de Partners",
#     layout="wide"
# )


# # ==================================
# # CONEXIÓN A POSTGRESQL (Neon.tech)
# # ==================================

# from src.data_loader import load_data

# st.sidebar.info("🔄 Cargando datos desde Neon.tech...")
# partners, countries, plans, statuses, notifications = load_data()
# st.sidebar.success("🟢 Datos cargados correctamente")

# # =============================
# # CARGA DE DATOS
# # =============================

# test_query = "SELECT NOW();"
# try:
#     cur = conn.cursor()
#     cur.execute(test_query)
#     result = cur.fetchone()
#     cur.close()
#     st.sidebar.success(f"🟢 Conectado a Neon.tech ({result[0]})")

# except psycopg2.InterfaceError:
#     st.sidebar.warning("♻️ Conexión cerrada, reabriendo...")
#     try:
#         conn = init_connection()
#         cur = conn.cursor()
#         cur.execute(test_query)
#         result = cur.fetchone()
#         cur.close()
#         st.sidebar.success(f"🟢 Reconectado a Neon.tech ({result[0]})")
#     except Exception as e:
#         st.sidebar.error(f"❌ Error reconectando a Neon.tech: {e}")

# except Exception as e:
#     st.sidebar.error(f"⚠️ Error verificando conexión: {e}")

# # Limpieza manual opcional de caché (solo durante desarrollo)
# # st.cache_data.clear()

# partners, countries, plans, statuses, notifications = load_data()




# # =============================
# # PREPARACIÓN / MERGE
# # =============================
# merged = (
#     partners
#     .merge(countries, left_on="country_id", right_on="id_country")
#     .merge(plans,     left_on="plan_id",     right_on="id_plan")
#     .merge(statuses,  left_on="status_id",   right_on="id_status")
# )

# merged.rename(columns={
#     "partner_name": "Partner",
#     "country_name": "País",
#     "plan_name":    "Plan",
#     "status_name":  "Estado",
#     "join_date":    "FechaAlta"
# }, inplace=True)

# merged["FechaAlta"] = pd.to_datetime(merged["FechaAlta"])

# # =============================
# # THEME / PALETA
# # =============================
# COLOR_PALETTE = ['#349ce4', '#1c4c74', '#6cb4e4', '#648cac', '#354551', '#b2b6b0']
# BACKGROUND_COLOR = "#0E1117"   # fondo oscuro estilo Streamlit dark
# TEXT_COLOR = "#E0E0E0"
# GRID_COLOR = "#333"

# def apply_dark_theme(fig):
#     fig.update_layout(
#         paper_bgcolor=BACKGROUND_COLOR,
#         plot_bgcolor=BACKGROUND_COLOR,
#         font=dict(color=TEXT_COLOR),
#         title_font=dict(size=18, color="#6cb4e4"),
#         xaxis=dict(color=TEXT_COLOR, gridcolor=GRID_COLOR),
#         yaxis=dict(color=TEXT_COLOR, gridcolor=GRID_COLOR),
#         legend=dict(font=dict(color=TEXT_COLOR))
#     )
#     return fig

# # =============================
# # SIDEBAR: FILTROS
# # =============================
# st.sidebar.header("Filtros")

# # Filtro País
# paises_unicos = sorted(merged["País"].unique().tolist())
# opcion_pais = st.sidebar.selectbox(
#     " País",
#     options=["Todos"] + paises_unicos,
#     index=0
# )

# # Filtro Plan
# planes_unicos = sorted(merged["Plan"].unique().tolist())
# opcion_plan = st.sidebar.selectbox(
#     " Plan Comercial",
#     options=["Todos"] + planes_unicos,
#     index=0
# )

# # Filtro Rango de Fechas
# fecha_min = merged["FechaAlta"].min()
# fecha_max = merged["FechaAlta"].max()

# rango_fecha = st.sidebar.date_input(
#     " Rango de Fecha de Alta",
#     value=(fecha_min, fecha_max),
#     min_value=fecha_min,
#     max_value=fecha_max
# )

# # Normalizamos types del filtro de fechas
# fecha_inicio = pd.to_datetime(rango_fecha[0])
# fecha_fin    = pd.to_datetime(rango_fecha[1]) + pd.Timedelta(days=1)  # incluye fin

# # =============================
# # APLICAMOS LOS FILTROS
# # =============================
# filtered = merged.copy()

# if opcion_pais != "Todos":
#     filtered = filtered[filtered["País"] == opcion_pais]

# if opcion_plan != "Todos":
#     filtered = filtered[filtered["Plan"] == opcion_plan]

# filtered = filtered[
#     (filtered["FechaAlta"] >= fecha_inicio) &
#     (filtered["FechaAlta"] <  fecha_fin)
# ].copy()

# # Para panel operativo usamos notif + partners originales (sin filtro de país/plan),
# # pero si querés también filtrar por país/plan necesitaríamos mergear notif con filtered.
# notif_full = (
#     notifications
#     .merge(partners, left_on="partner_id", right_on="id_partner")
#     .merge(plans,    left_on="plan_id",    right_on="id_plan")
# )

# # ============================================================
# # CREACIÓN DE DATAFRAMES DERIVADOS (ANTES DE USARLOS)
# # ============================================================

# # Aseguramos columna MesAlta y DataFrame evolución
# if not filtered.empty and "FechaAlta" in filtered.columns:
#     filtered["MesAlta"] = filtered["FechaAlta"].dt.to_period("M").astype(str)
#     evolucion = (
#         filtered.groupby("MesAlta")["Partner"]
#         .count()
#         .reset_index()
#         .rename(columns={"Partner": "NuevosPartners"})
#         .sort_values("MesAlta")
#     )
# else:
#     evolucion = pd.DataFrame(columns=["MesAlta", "NuevosPartners"])


# # =============================
# # HEADER (título)
# # =============================
# st.markdown(
#     f"""
#     <h1 style="color:#E0E0E0; margin-bottom:0;"> Sistema de Partners </h1>
#     <p style="color:#b2b6b0; margin-top:4px;">
#     Vista ejecutiva y operativa de la red de partners. <br/>
#     Los filtros de la izquierda impactan en todas las métricas excepto las operativas globales de notificaciones.
#     </p>
#     """,
#     unsafe_allow_html=True
# )

# # ============================================================
# # FECHA Y HORA DE ACTUALIZACIÓN (hora local del visitante)
# # ============================================================
# st.components.v1.html(
#     """
#     <div id="update-time" style="color:#6cb4e4; font-size:14px; margin-top:-10px;">
#         🔄 Actualizando datos...
#     </div>
#     <script>
#         // Esperamos unos segundos para simular carga de datos
#         setTimeout(() => {
#             const now = new Date();
#             const options = {
#                 year: 'numeric', month: '2-digit', day: '2-digit',
#                 hour: '2-digit', minute: '2-digit', second: '2-digit'
#             };
#             const localTime = now.toLocaleString([], options);
#             document.getElementById("update-time").innerHTML = 
#                 "📅 Datos actualizados al " + localTime;
#         }, 1500);
#     </script>
#     """,
#     height=40
# )


# # ============================================================
# # NIVEL 1 — VISIÓN GENERAL (tarjetas KPI)
# # ============================================================

# total_partners      = len(filtered)
# activos_partners    = len(filtered[filtered["Estado"] == "Activo"])
# inactivos_partners  = len(filtered[filtered["Estado"] != "Activo"])
# prom_notif_global   = notifications["notification_count"].mean().round(2)

# col_kpi1, col_kpi2, col_kpi3, col_kpi4 = st.columns(4)

# with col_kpi1:
#     st.metric(" Total de Partners", total_partners)

# with col_kpi2:
#     st.metric(" Partners Activos", activos_partners)

# with col_kpi3:
#     st.metric(" Partners No Activos", inactivos_partners)

# with col_kpi4:
#     st.metric(" Promedio Notificaciones (global)", prom_notif_global)

# st.markdown("---")


# # ============================================================
# # NIVEL 2 — DISTRIBUCIÓN ALTA NIVEL
# #    - Estado (Activos vs No Activos)
# #    - Distribución geográfica
# # ============================================================

# col_dist1, col_dist2 = st.columns(2)

# # 2A. Estado (pie activos vs no activos)
# estado_counts = (
#     filtered
#     .assign(Activo=lambda df: df["Estado"] == "Activo")
#     .replace({True: "Activo", False: "No Activo"})
#     .groupby("Activo")["Partner"]
#     .count()
#     .reset_index()
#     .rename(columns={"Partner": "Cantidad", "Activo": "Estado"})
# )

# fig_estado = px.pie(
#     estado_counts,
#     names="Estado",
#     values="Cantidad",
#     title="Distribución Partners Activos vs No Activos",
#     color_discrete_sequence=COLOR_PALETTE
# )
# fig_estado.update_traces(textinfo="percent+label", pull=[0.05, 0.05])
# apply_dark_theme(fig_estado)
# col_dist1.plotly_chart(fig_estado, use_container_width=True)

# # 2B. Distribución geográfica (barras horizontales)
# geo_counts = (
#     filtered
#     .groupby("País")["Partner"]
#     .count()
#     .reset_index()
#     .sort_values("Partner", ascending=True)
# )

# fig_geo = px.bar(
#     geo_counts,
#     x="Partner",
#     y="País",
#     orientation="h",
#     text="Partner",
#     color="País",
#     title="Partners por País",
#     color_discrete_sequence=COLOR_PALETTE,
#     labels={"Partner": "Cantidad de Partners", "País": "País"}
# )
# fig_geo.update_traces(textposition="outside")
# apply_dark_theme(fig_geo)
# col_dist2.plotly_chart(fig_geo, use_container_width=True)

# st.markdown("---")

# # ============================================================
# # NIVEL 3 — EVOLUCIÓN TEMPORAL / TENDENCIA
# #    - Altas mensuales
# # ============================================================

# filtered["MesAlta"] = filtered["FechaAlta"].dt.to_period("M").astype(str)
# evolucion = (
#     filtered
#     .groupby("MesAlta")["Partner"]
#     .count()
#     .reset_index()
#     .rename(columns={"Partner": "NuevosPartners"})
#     .sort_values("MesAlta")
# )

# fig_evol = px.line(
#     evolucion,
#     x="MesAlta",
#     y="NuevosPartners",
#     title="Evolución de Altas Mensuales",
#     markers=True,
#     labels={"MesAlta": "Mes de Alta", "NuevosPartners": "Cantidad de Nuevos Partners"}
# )
# fig_evol.update_traces(line_color="#349ce4", marker_color="#6cb4e4")
# apply_dark_theme(fig_evol)

# st.plotly_chart(fig_evol, use_container_width=True)

# st.markdown("---")

# # ============================================================
# # NIVEL 4 — ANÁLISIS POR PLAN Y TOP PARTNERS
# # ============================================================

# col_plan, col_top = st.columns(2)

# # 4A. Partners activos por plan (solo filtrados)
# activos_filtrados = filtered[filtered["Estado"] == "Activo"]
# planes_counts = (
#     activos_filtrados
#     .groupby("Plan")["Partner"]
#     .count()
#     .reset_index()
#     .rename(columns={"Partner": "PartnersActivos"})
#     .sort_values("PartnersActivos", ascending=False)
# )

# fig_plan = px.bar(
#     planes_counts,
#     x="Plan",
#     y="PartnersActivos",
#     color="Plan",
#     title="Partners Activos por Plan Comercial",
#     color_discrete_sequence=COLOR_PALETTE,
#     labels={"Plan": "Plan Comercial", "PartnersActivos": "Partners Activos"}
# )
# apply_dark_theme(fig_plan)
# col_plan.plotly_chart(fig_plan, use_container_width=True)

# # 4B. Top 10 partners por notificaciones (global)
# top_notif = (
#     notif_full
#     .groupby("partner_name")["notification_count"]
#     .sum()
#     .reset_index()
#     .sort_values("notification_count", ascending=False)
#     .head(10)
# )
# fig_top = px.bar(
#     top_notif,
#     x="partner_name",
#     y="notification_count",
#     color="notification_count",
#     title="Top 10 Partners por Volumen de Notificaciones",
#     color_continuous_scale=COLOR_PALETTE,
#     labels={"partner_name": "Partner", "notification_count": "Total Notificaciones"}
# )
# apply_dark_theme(fig_top)
# col_top.plotly_chart(fig_top, use_container_width=True)

# st.markdown("---")

# # ============================================================
# # NIVEL 5 — DISTRIBUCIÓN DE PARTNERS POR INDUSTRIA (con filtros)
# # ============================================================

# st.markdown(
#     "<h3 style='color:#6cb4e4;'>🏭 Distribución de Partners por Industria</h3>",
#     unsafe_allow_html=True
# )

# # Aplicamos los mismos filtros (ya vienen de "filtered")
# if "industry" in filtered.columns and not filtered.empty:
#     industria_counts = (
#         filtered
#         .groupby("industry")["Partner"]
#         .count()
#         .reset_index()
#         .rename(columns={"industry": "Industria", "Partner": "Cantidad"})
#         .sort_values("Cantidad", ascending=False)
#     )

#     fig_industria = px.bar(
#         industria_counts,
#         x="Industria",
#         y="Cantidad",
#         color="Industria",
#         title="Cantidad de Partners por Industria (según filtros aplicados)",
#         text="Cantidad",
#         color_discrete_sequence=COLOR_PALETTE
#     )

#     fig_industria.update_traces(textposition="outside")
#     apply_dark_theme(fig_industria)
#     st.plotly_chart(fig_industria, use_container_width=True, key="ind_chart")

# else:
#     st.info("⚠️ No hay datos disponibles para la industria según los filtros actuales.")





# # ============================================================
# # NIVEL 6 — MAPA GEOGRÁFICO DE PARTNERS EN AMÉRICA
# # ============================================================

# st.markdown(
#     "<h3 style='color:#6cb4e4;'>🌎 Distribución Geográfica de Partners en América</h3>",
#     unsafe_allow_html=True
# )

# # Agrupamos cantidad de partners por país
# map_data = (
#     merged.groupby("País")["Partner"]
#     .count()
#     .reset_index()
#     .rename(columns={"Partner": "CantidadPartners"})
# )

# # Corrección opcional de nombres de países
# map_data["País"] = map_data["País"].replace({
#     "Estados Unidos": "United States of America",
#     "USA": "United States",
#     "México": "Mexico",
#     "Argentina": "Argentina",
#     "Colombia": "Colombia",
#     "Brasil": "Brazil",
#     "Chile": "Chile",
#     "Perú": "Peru",
#     "Uruguay": "Uruguay",
#     "Paraguay": "Paraguay",
#     "Bolivia": "Bolivia",
#     "Ecuador": "Ecuador",
#     "Venezuela": "Venezuela",
#     "Costa Rica": "Costa Rica",
#     "Panamá": "Panama",
#     "Canadá": "Canada"
# })

# # Mapa coroplético centrado en América completa
# fig_map = px.choropleth(
#     map_data,
#     locations="País",
#     locationmode="country names",
#     color="CantidadPartners",
#     color_continuous_scale="blues",
#     title="Cantidad de Partners por País en América",
#     labels={"CantidadPartners": "Partners"},
# )

# fig_map.update_layout(
#     geo=dict(
#         projection_type="natural earth",   # proyección más natural
#         scope="world",             # muestra América del Sur
#         lonaxis_range=[-170, -30],         # ajusta el rango de longitud
#         lataxis_range=[-60, 75],           # incluye toda América del Norte y Sur
#         showframe=False,
#         showcoastlines=True,
#         coastlinecolor="#555",
#         landcolor="#1c1c1c",
#         bgcolor=BACKGROUND_COLOR
#     ),
#     paper_bgcolor=BACKGROUND_COLOR,
#     font=dict(color=TEXT_COLOR),
#     title_font=dict(size=18, color="#6cb4e4"),
# )

# st.plotly_chart(fig_map, use_container_width=True)


# # ============================================================
# # NIVEL 7 — KPIs AVANZADOS Y CORRELACIÓN DE VARIABLES
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



# # ============================================================
# # INSIGHTS FINALES — Dinámicos según los datos actuales
# # ============================================================
# st.markdown(
#     "<h3 style='color:#6cb4e4;'>✅ Insights Clave</h3>",
#     unsafe_allow_html=True
# )

# insights = []

# # ---- Utilidades seguras ----
# def safe_vc_top(s, default=("Sin datos", 0)):
#     if s is None:
#         return default
#     vc = s.value_counts()
#     if vc.empty:
#         return default
#     return vc.idxmax(), int(vc.max())

# def fmt_pct(num, den):
#     return f"{(num/den*100):.1f}%" if den and den > 0 else "0.0%"

# # ---- 1) Estado general y actividad ----
# total_partners = len(filtered)
# activos_partners = len(filtered[filtered["Estado"] == "Activo"])
# porc_activos = fmt_pct(activos_partners, total_partners)

# if total_partners > 0:
#     insights.append(
#         f"La red filtrada cuenta con <b>{total_partners}</b> partners, de los cuales "
#         f"<b>{activos_partners}</b> están activos (<b>{porc_activos}</b>)."
#     )
# else:
#     insights.append("No hay partners para los filtros actuales.")

# # ---- 2) País/mercado líder (por volumen en el período) ----
# pais_top, pais_top_cnt = safe_vc_top(filtered["País"])
# if pais_top != "Sin datos":
#     insights.append(
#         f"El mercado con mayor presencia es <b>{pais_top}</b>, con <b>{pais_top_cnt}</b> partners en el período seleccionado."
#     )

# # ---- 3) Tendencia de crecimiento (evolución mensual) ----
# # Reusa 'evolucion' si existe; si no, la calculamos rápido
# if "evolucion" not in locals() or evolucion is None or evolucion.empty:
#     if not filtered.empty:
#         tmp = filtered.copy()
#         tmp["MesAlta"] = tmp["FechaAlta"].dt.to_period("M").astype(str)
#         evolucion = (
#             tmp.groupby("MesAlta")["Partner"]
#             .count()
#             .reset_index()
#             .rename(columns={"Partner": "NuevosPartners"})
#             .sort_values("MesAlta")
#         )
#     else:
#         evolucion = pd.DataFrame(columns=["MesAlta", "NuevosPartners"])

# if len(evolucion) >= 2:
#     altas_mes_actual = int(evolucion["NuevosPartners"].iloc[-1])
#     altas_mes_prev   = int(evolucion["NuevosPartners"].iloc[-2])
#     tasa_crecimiento = ((altas_mes_actual - altas_mes_prev) / altas_mes_prev * 100) if altas_mes_prev > 0 else 0.0
#     tendencia = "alza 📈" if tasa_crecimiento > 0 else ("baja 📉" if tasa_crecimiento < 0 else "estable ⚖️")
#     insights.append(
#         f"El ritmo de altas mensuales muestra una tendencia de <b>{tendencia}</b>: "
#         f"{altas_mes_actual} vs {altas_mes_prev} (Δ {tasa_crecimiento:.1f}%)."
#     )
# elif len(evolucion) == 1:
#     insights.append(
#         f"Se registraron <b>{int(evolucion['NuevosPartners'].iloc[-1])}</b> altas en el único mes del rango seleccionado."
#     )

# # ---- 4) Plan comercial predominante ----
# plan_top, plan_top_cnt = safe_vc_top(filtered["Plan"])
# if plan_top != "Sin datos":
#     insights.append(
#         f"El plan con mayor adopción es <b>{plan_top}</b> con <b>{plan_top_cnt}</b> partners, "
#         f"indicando preferencia por esa propuesta de valor."
#     )

# # ---- 5) Industria predominante (sobre el conjunto filtrado) ----
# if "industry" in filtered.columns and not filtered.empty:
#     ind_top, ind_top_cnt = safe_vc_top(filtered["industry"])
#     if ind_top != "Sin datos":
#         insights.append(
#             f"La industria más representada es <b>{ind_top}</b> con <b>{ind_top_cnt}</b> registros, "
#             f"lo que sugiere foco de captación en ese segmento."
#         )

# # ---- 6) Interacción/engagement (notificaciones) ----
# # Promedio global ya existe como 'prom_notif_global' (no filtrado); calculamos filtrado también:
# try:
#     notif_filtrado = (
#         notifications
#         .merge(partners, left_on="partner_id", right_on="id_partner")
#         .merge(plans,    left_on="plan_id",    right_on="id_plan")
#         .merge(filtered[["Partner"]], left_on="partner_name", right_on="Partner", how="inner")
#     )
#     prom_notif_filtrado = float(notif_filtrado["notification_count"].mean()) if not notif_filtrado.empty else 0.0
# except Exception:
#     prom_notif_filtrado = 0.0

# if prom_notif_filtrado > 0:
#     insights.append(
#         f"El nivel de interacción promedio (notificaciones) para el subconjunto filtrado es de "
#         f"<b>{prom_notif_filtrado:.1f}</b> por partner."
#     )

# # ---- 7) Señales para la acción (oportunidades) ----
# # Países con baja presencia relativa (bottom 3, si hay suficientes)
# geo_counts = (
#     filtered.groupby("País")["Partner"].count().reset_index().sort_values("Partner", ascending=True)
#     if not filtered.empty else pd.DataFrame(columns=["País","Partner"])
# )
# if len(geo_counts) >= 3:
#     low_markets = ", ".join(geo_counts.head(3)["País"].tolist())
#     insights.append(
#         f"Se detectan oportunidades de expansión en mercados con menor representación: <b>{low_markets}</b>."
#     )

# # ---- Render final ----
# if insights:
#     html = "<ul style='color:#E0E0E0; font-size:15px; line-height:1.5;'>"
#     for li in insights:
#         html += f"<li>{li}</li>"
#     html += "</ul>"
#     st.markdown(html, unsafe_allow_html=True)
# else:
#     st.info("No hay insights disponibles para los filtros seleccionados.")


# # =====================================================
# # BOTÓN PARA ABRIR PÁGINA DEL MODELO (COMPATIBLE Y FUNCIONAL)
# # =====================================================

# # import streamlit as st

# # # Intentar obtener la URL base automáticamente (compatible)
# # try:
# #     base_url = st.runtime.scriptrunner.get_script_run_ctx().streamlit_script_run_ctx.session_data.browser_host
# #     modelo_url = f"http://{base_url}/modelo"
# # except Exception:
# #     # Si no se puede detectar, usa el puerto por defecto
# #     modelo_url = "http://localhost:8501/modelo"

# # # Render del botón con estilo
# # st.markdown(f"""
# #     <style>
# #     .open-model-btn {{
# #         display: block;
# #         margin: 50px auto 100px auto;
# #         background-color: #2d2f33;
# #         color: #f0f2f6;
# #         border: none;
# #         border-radius: 12px;
# #         padding: 14px 35px;
# #         font-size: 17px;
# #         font-weight: 600;
# #         cursor: pointer;
# #         transition: all 0.3s ease;
# #         text-decoration: none;
# #         text-align: center;
# #         box-shadow: 0px 2px 6px rgba(0, 0, 0, 0.3);
# #     }}
# #     .open-model-btn:hover {{
# #         background-color: #4f9bee;
# #         color: white;
# #         transform: translateY(-3px);
# #         box-shadow: 0px 4px 12px rgba(79, 155, 238, 0.6);
# #     }}
# #     </style>

# #     <div style='text-align: center;'>
# #         <a href='{modelo_url}' target='_blank' class='open-model-btn'>
# #             🧠 Ver modelo de Machine Learning
# #         </a>
# #     </div>
# # """, unsafe_allow_html=True)


# st.markdown("---")
# st.subheader("🔍 Análisis avanzado")

# # 🔗 Navegación interna (requiere Streamlit >=1.24)
# st.page_link("pages/modelo.py", label="🧠 Ver modelo de Machine Learning", icon="🤖")

# st.markdown("---")
# st.markdown("<p style='text-align:center; color:gray;'>© 2025 | Desarrollado por Fernando Raúl Robles</p>", unsafe_allow_html=True)




# try:
#     show()   # o main(), dependiendo de cómo se llame tu función principal
# except Exception as e:
#     st.error(f"❌ Error en la app: {e}")
#     st.code(traceback.format_exc())



# ====================================================
# DASHBOARD - Sistema de Partners (SimiAI)
# Dashboard analítico desarrollado en Streamlit.
# Autor: Fernando Raúl Robles
# Fecha: 27/10/2025
# ====================================================

import streamlit as st
import pandas as pd
import psycopg2
import plotly.express as px
import datetime
import traceback

# Módulos internos
from src.db_connection import init_connection
from src.data_loader import load_data


# =============================
# CONFIG BASE
# =============================
st.set_page_config(
    page_title="Sistema de Partners",
    layout="wide"
)

# =============================
# CONEXIÓN A NEON.tech
# =============================
st.sidebar.info("🔄 Conectando a Neon.tech...")

try:
    conn = init_connection()
    cur = conn.cursor()
    cur.execute("SELECT NOW();")
    now_res = cur.fetchone()[0]
    cur.close()
    st.sidebar.success(f"🟢 Conectado a Neon.tech ({now_res})")
except Exception as e:
    st.sidebar.error(f"❌ Error conectando: {e}")

# =============================
# CARGA DE DATOS
# =============================
st.sidebar.info("📥 Cargando datos...")
partners, countries, plans, statuses, notifications = load_data()
st.sidebar.success("🟢 Datos cargados correctamente")


# =============================
# MERGE PRINCIPAL
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
# PALETA DARK
# =============================
COLOR_PALETTE = ['#349ce4', '#1c4c74', '#6cb4e4', '#648cac', '#354551']
BACKGROUND_COLOR = "#0E1117"
TEXT_COLOR = "#E0E0E0"
GRID_COLOR = "#333"

def apply_dark_theme(fig):
    fig.update_layout(
        paper_bgcolor=BACKGROUND_COLOR,
        plot_bgcolor=BACKGROUND_COLOR,
        font=dict(color=TEXT_COLOR),
        xaxis=dict(color=TEXT_COLOR, gridcolor=GRID_COLOR),
        yaxis=dict(color=TEXT_COLOR, gridcolor=GRID_COLOR),
        title_font=dict(color="#6cb4e4")
    )
    return fig


# =============================
# SIDEBAR — FILTROS
# =============================
st.sidebar.header("Filtros")

opcion_pais = st.sidebar.selectbox(
    "País", ["Todos"] + sorted(merged["País"].unique())
)

opcion_plan = st.sidebar.selectbox(
    "Plan Comercial", ["Todos"] + sorted(merged["Plan"].unique())
)

fecha_min = merged["FechaAlta"].min()
fecha_max = merged["FechaAlta"].max()

rango_fecha = st.sidebar.date_input(
    "Rango de Fecha de Alta",
    value=(fecha_min, fecha_max),
    min_value=fecha_min,
    max_value=fecha_max
)

fecha_inicio = pd.to_datetime(rango_fecha[0])
fecha_fin    = pd.to_datetime(rango_fecha[1]) + pd.Timedelta(days=1)


# =============================
# APLICAR FILTROS
# =============================
filtered = merged.copy()

if opcion_pais != "Todos":
    filtered = filtered[filtered["País"] == opcion_pais]

if opcion_plan != "Todos":
    filtered = filtered[filtered["Plan"] == opcion_plan]

filtered = filtered[
    (filtered["FechaAlta"] >= fecha_inicio) &
    (filtered["FechaAlta"] < fecha_fin)
].copy()


# =============================
# HEADERS
# =============================
st.markdown(
    """
    <h1 style="color:#E0E0E0;">Sistema de Partners</h1>
    <p style="color:#b2b6b0;">
        Dashboard ejecutivo y operativo según la actividad de los partners.
    </p>
    """,
    unsafe_allow_html=True
)

# =============================
# FECHA DE ACTUALIZACIÓN
# =============================
st.components.v1.html(
    """
    <div id="update-time" style="color:#6cb4e4;">
        🔄 Actualizando datos...
    </div>
    <script>
        setTimeout(() => {
            const now = new Date().toLocaleString();
            document.getElementById("update-time").innerHTML =
                "📅 Datos actualizados al " + now;
        }, 1000);
    </script>
    """,
    height=40
)


# =============================
# KPIs PRINCIPALES
# =============================
total_partners = len(filtered)
activos = len(filtered[filtered["Estado"] == "Activo"])
inactivos = total_partners - activos
prom_notif_global = notifications["notification_count"].mean().round(2)

c1, c2, c3, c4 = st.columns(4)
c1.metric("Total de Partners", total_partners)
c2.metric("Activos", activos)
c3.metric("No Activos", inactivos)
c4.metric("Prom Notificaciones", prom_notif_global)

st.markdown("---")


# =============================
# 1 — Activos vs No activos
# =============================
estado_counts = (
    filtered
    .assign(Activo=(filtered["Estado"] == "Activo"))
    .replace({True: "Activo", False: "No Activo"})
    .groupby("Activo")["Partner"]
    .count()
    .reset_index()
)

fig_estado = px.pie(
    estado_counts,
    names="Activo",
    values="Partner",
    title="Distribución por Estado",
    color_discrete_sequence=COLOR_PALETTE
)
apply_dark_theme(fig_estado)

col1, col2 = st.columns(2)
col1.plotly_chart(fig_estado, use_container_width=True)


# =============================
# 2 — Partners por País
# =============================
geo_counts = (
    filtered
    .groupby("País")["Partner"]
    .count()
    .reset_index()
)

fig_geo = px.bar(
    geo_counts,
    y="País",
    x="Partner",
    orientation="h",
    title="Partners por País",
    color="País",
    color_discrete_sequence=COLOR_PALETTE
)
apply_dark_theme(fig_geo)
col2.plotly_chart(fig_geo, use_container_width=True)

st.markdown("---")


# =============================
# 3 — Evolución mensual
# =============================
filtered["MesAlta"] = filtered["FechaAlta"].dt.to_period("M").astype(str)

evol = (
    filtered.groupby("MesAlta")["Partner"]
    .count()
    .reset_index()
    .rename(columns={"Partner": "Nuevos"})
    .sort_values("MesAlta")
)

fig_evol = px.line(
    evol,
    x="MesAlta",
    y="Nuevos",
    markers=True,
    title="Evolución de Nuevos Partners"
)
apply_dark_theme(fig_evol)
st.plotly_chart(fig_evol, use_container_width=True)

st.markdown("---")


# =============================
# 4 — Partners por Plan
# =============================
activos_filt = filtered[filtered["Estado"] == "Activo"]
plan_counts = (
    activos_filt.groupby("Plan")["Partner"]
    .count().reset_index()
)

fig_plan = px.bar(
    plan_counts,
    x="Plan",
    y="Partner",
    color="Plan",
    title="Partners Activos por Plan",
    color_discrete_sequence=COLOR_PALETTE
)
apply_dark_theme(fig_plan)
st.plotly_chart(fig_plan, use_container_width=True)

st.markdown("---")


# =============================
# Mapa Geográfico (América)
# =============================
map_data = (
    merged.groupby("País")["Partner"]
    .count()
    .reset_index()
    .rename(columns={"Partner": "Cantidad"})
)

map_data["País"] = map_data["País"].replace({
    "Estados Unidos": "United States",
    "México": "Mexico",
    "Brasil": "Brazil",
    "Perú": "Peru",
    "Costa Rica": "Costa Rica",
    "Panamá": "Panama"
})

fig_map = px.choropleth(
    map_data,
    locations="País",
    locationmode="country names",
    color="Cantidad",
    color_continuous_scale="blues",
    title="Partners por País"
)
apply_dark_theme(fig_map)
st.plotly_chart(fig_map, use_container_width=True)

st.markdown("---")


# =============================
# LINK A LA PÁGINA DEL MODELO
# =============================
st.page_link("pages/modelo.py", label="🧠 Ver modelo de Machine Learning")

st.markdown("---")
st.markdown(
    "<p style='text-align:center; color:gray;'>© 2025 | Desarrollado por Fernando Raúl Robles</p>",
    unsafe_allow_html=True
)

