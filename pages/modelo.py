# # ============================================================
# # MODELO ML - Proyecto SimiAI
# # Autor: Fernando Raúl Robles
# # Fecha: 05/11/2025
# # Descripción:
# # Visualización y análisis del modelo de Machine Learning
# # ============================================================

# import streamlit as st
# import pandas as pd
# import plotly.express as px
# import joblib
# import os

# # ------------------------------------------------------------
# # CONFIGURACIÓN INICIAL
# # ------------------------------------------------------------
# st.set_page_config(page_title="Modelo ML", page_icon="🧠", layout="wide")

# st.title("🧠 Modelo de Machine Learning - Predicción de Churn")
# st.markdown(
#     "Exploración del modelo **RandomForestClassifier** entrenado sobre la base de datos de *Partners SimiAI*."
# )
# st.markdown("---")

# # ------------------------------------------------------------
# # RUTAS RELATIVAS DE ARCHIVOS (dentro del repo)
# # ------------------------------------------------------------
# MODEL_PATH = "ml/modelo_churn.joblib"
# CSV_PATH = "ml/churn_results.csv"

# # ------------------------------------------------------------
# # INTENTO DE CARGA DE MODELO Y DATOS
# # ------------------------------------------------------------
# model = None
# df = None

# # Intentar cargar el modelo .joblib
# if os.path.exists(MODEL_PATH):
#     try:
#         model = joblib.load(MODEL_PATH)
#         st.success("✅ Modelo cargado correctamente.")
#     except Exception as e:
#         st.warning(
#             f"⚠️ No se pudo cargar el modelo (.joblib). Se mostrará solo el análisis del CSV.\n\n**Detalle:** {e}"
#         )
# else:
#     st.info("ℹ️ No se encontró el archivo `modelo_churn.joblib`. Solo se mostrarán los datos del CSV.")

# # Intentar cargar el CSV de resultados
# if os.path.exists(CSV_PATH):
#     try:
#         df = pd.read_csv(CSV_PATH)
#         st.success("✅ Datos de predicción cargados correctamente.")
#     except Exception as e:
#         st.error(f"❌ Error al cargar el archivo CSV: {e}")
#         st.stop()
# else:
#     st.error("⚠️ No se encontró el archivo 'churn_results.csv'.")
#     st.stop()

# # ------------------------------------------------------------
# # MÉTRICAS PRINCIPALES
# # ------------------------------------------------------------
# st.markdown("### 📊 Métricas principales")

# col1, col2, col3 = st.columns(3)
# churn_rate = df["churn"].mean() if "churn" in df.columns else 0
# avg_prob = df["prob_churn"].mean() if "prob_churn" in df.columns else 0
# total_partners = len(df)

# col1.metric("Total de Partners", f"{total_partners}")
# col2.metric("Tasa de Churn Real", f"{churn_rate:.2%}")
# col3.metric("Probabilidad Promedio de Churn", f"{avg_prob:.2%}")

# st.markdown("---")

# # ------------------------------------------------------------
# # VISUALIZACIONES PRINCIPALES
# # ------------------------------------------------------------
# st.subheader("📈 Distribución de probabilidad de churn")

# if "prob_churn" in df.columns:
#     fig = px.histogram(
#         df,
#         x="prob_churn",
#         nbins=25,
#         title="Distribución de probabilidades de churn",
#         color_discrete_sequence=["#4f9bee"],
#     )
#     st.plotly_chart(fig, use_container_width=True)
# else:
#     st.info("No se encontró la columna `prob_churn` en el dataset.")

# # ------------------------------------------------------------
# # TOP 10 PARTNERS EN RIESGO
# # ------------------------------------------------------------
# if all(col in df.columns for col in ["partner_name", "prob_churn"]):
#     st.subheader("⚠️ Top 10 Partners con mayor probabilidad de churn")
#     risky = df.sort_values("prob_churn", ascending=False).head(10)
#     st.dataframe(
#         risky[["partner_name", "plan_name", "status_name", "prob_churn"]],
#         use_container_width=True,
#     )

# # ------------------------------------------------------------
# # CHURN PROMEDIO POR PLAN
# # ------------------------------------------------------------
# if all(col in df.columns for col in ["plan_name", "prob_churn"]):
#     st.subheader("📊 Tasa promedio de churn por plan")
#     churn_plan = df.groupby("plan_name")["prob_churn"].mean().reset_index()
#     fig2 = px.bar(
#         churn_plan,
#         x="plan_name",
#         y="prob_churn",
#         title="Promedio de churn por plan",
#         text_auto=".2%",
#         color="plan_name",
#         color_discrete_sequence=["#4f9bee"],
#     )
#     st.plotly_chart(fig2, use_container_width=True)

# # ------------------------------------------------------------
# # IMPORTANCIA DE VARIABLES (solo si el modelo se cargó)
# # ------------------------------------------------------------
# if model is not None and hasattr(model, "feature_importances_"):
#     st.subheader("🧩 Importancia de variables")
#     importances = pd.Series(model.feature_importances_, index=model.feature_names_in_)
#     importances = importances.sort_values(ascending=True)
#     fig_imp = px.bar(
#         importances,
#         orientation="h",
#         title="Importancia de características",
#         color_discrete_sequence=["#4f9bee"],
#     )
#     st.plotly_chart(fig_imp, use_container_width=True)
# elif model is None:
#     st.info("ℹ️ El modelo no está disponible; se omite la importancia de variables.")
# else:
#     st.info("ℹ️ Este modelo no contiene información de importancia de variables.")

# # ------------------------------------------------------------
# # PIE DE PÁGINA
# # ------------------------------------------------------------
# st.markdown("---")
# st.markdown(
#     "<p style='text-align:center; color:gray;'>© 2025 | Desarrollado por <b>Fernando Raúl Robles</b></p>",
#     unsafe_allow_html=True,
# )


# ============================================================
# 🧠 MODELO ML – Predicción de Bajas (Churn)
# Autor: Fernando Raúl Robles
# Fecha: 05/11/2025
# ============================================================

import streamlit as st
import pandas as pd
import plotly.express as px
import joblib
import os

# ------------------------------------------------------------
# CONFIGURACIÓN INICIAL
# ------------------------------------------------------------
st.set_page_config(page_title="Modelo ML - Bajas", page_icon="📉", layout="wide")

st.title("🧠 Modelo de Machine Learning – Predicción de Bajas")
st.markdown(
    "Dashboard de análisis del modelo **RandomForestClassifier** encargado de estimar la probabilidad de baja de los partners."
)
st.markdown("---")

# ------------------------------------------------------------
# RUTAS
# ------------------------------------------------------------
MODEL_PATH = "ml/modelo_churn.joblib"
CSV_PATH = "ml/churn_results.csv"

model = None
df = None

# ------------------------------------------------------------
# CARGA DEL MODELO
# ------------------------------------------------------------
if os.path.exists(MODEL_PATH):
    try:
        model = joblib.load(MODEL_PATH)
        st.success("✅ Modelo cargado correctamente.")
    except Exception as e:
        st.warning(f"⚠️ No se pudo cargar el modelo.\n\n**Detalle:** {e}")
else:
    st.info("ℹ️ No se encontró el archivo `modelo_churn.joblib`.")

# ------------------------------------------------------------
# CARGA DEL CSV
# ------------------------------------------------------------
if os.path.exists(CSV_PATH):
    try:
        df = pd.read_csv(CSV_PATH)
        st.success("✅ Datos de predicción cargados correctamente.")
    except Exception as e:
        st.error(f"❌ Error al cargar el CSV: {e}")
        st.stop()
else:
    st.error("⚠️ No se encontró el archivo 'churn_results.csv'.")
    st.stop()

# ------------------------------------------------------------
# RENOMBRADO DE COLUMNAS
# ------------------------------------------------------------
df = df.rename(columns={
    "prob_churn": "Probabilidad de baja",
    "plan_name": "Plan",
    "status_name": "Estado",
    "partner_name": "Partner"
})

# ------------------------------------------------------------
# MÉTRICAS PRINCIPALES
# ------------------------------------------------------------
st.markdown("### 📊 Indicadores principales")

col1, col2, col3 = st.columns(3)

tasa_baja = df["churn"].mean() if "churn" in df.columns else 0
prob_promedio = df["Probabilidad de baja"].mean()
total_partners = len(df)

col1.metric("Total de Partners", total_partners)
col2.metric("Tasa Real de Bajas", f"{tasa_baja:.2%}")
col3.metric("Probabilidad Promedio de Baja", f"{prob_promedio:.2%}")

st.markdown("---")

# ------------------------------------------------------------
# DISTRIBUCIÓN DE PROBABILIDAD DE BAJA
# ------------------------------------------------------------
st.subheader("📈 Distribución de probabilidad de baja")

fig = px.histogram(
    df,
    x="Probabilidad de baja",
    nbins=25,
    title="Distribución de probabilidad de baja",
    labels={
        "Probabilidad de baja": "Probabilidad de baja",
        "count": "Cantidad"
    },
    color_discrete_sequence=["#4f9bee"],
)
st.plotly_chart(fig, use_container_width=True)

# ------------------------------------------------------------
# TOP 10 PARTNERS EN RIESGO
# ------------------------------------------------------------
st.subheader("⚠️ Top 10 Partners con mayor probabilidad de baja")

if all(col in df.columns for col in ["Partner", "Probabilidad de baja"]):
    risky = df.sort_values("Probabilidad de baja", ascending=False).head(10)
    st.dataframe(
        risky[["Partner", "Plan", "Estado", "Probabilidad de baja"]],
        use_container_width=True,
    )
else:
    st.info("No se encontraron las columnas necesarias para mostrar esta sección.")

# ------------------------------------------------------------
# PROBABILIDAD DE BAJA POR PLAN
# ------------------------------------------------------------
st.subheader("📊 Probabilidad promedio de baja por plan")

if all(col in df.columns for col in ["Plan", "Probabilidad de baja"]):

    bajas_plan = df.groupby("Plan")["Probabilidad de baja"].mean().reset_index()

    fig2 = px.bar(
        bajas_plan,
        x="Plan",
        y="Probabilidad de baja",
        title="Probabilidad promedio de baja por plan",
        text_auto=".2%",
        labels={
            "Plan": "Plan",
            "Probabilidad de baja": "Probabilidad de baja"
        },
        color="Plan",
        color_discrete_sequence=["#4f9bee"],
    )
    st.plotly_chart(fig2, use_container_width=True)
else:
    st.info("No se encontraron columnas suficientes para calcular bajas promedio por plan.")

# ------------------------------------------------------------
# IMPORTANCIA DE VARIABLES (si existe)
# ------------------------------------------------------------
if model is not None and hasattr(model, "feature_importances_"):
    st.subheader("🧩 Importancia de Variables en el Modelo")

    # Intento seguro de obtener features
    if hasattr(model, "feature_names_in_"):
        columnas = model.feature_names_in_
    else:
        columnas = df.select_dtypes(include=["int64", "float64"]).columns

    importancias = pd.Series(model.feature_importances_, index=columnas).sort_values()

    fig_imp = px.bar(
        importancias,
        orientation="h",
        title="Importancia de características",
        labels={"value": "Importancia", "index": "Variable"},
        color_discrete_sequence=["#4f9bee"],
    )

    st.plotly_chart(fig_imp, use_container_width=True)

# Si no existe importancia:
elif model is None:
    st.info("ℹ️ El modelo no está disponible; se omite la importancia de variables.")
else:
    st.info("ℹ️ Este modelo no contiene información de importancia de variables.")

# ------------------------------------------------------------
# PIE DE PÁGINA
# ------------------------------------------------------------
st.markdown("---")
st.markdown(
    "<p style='text-align:center; color:gray;'>© 2025 | Desarrollado por <b>Fernando Raúl Robles</b></p>",
    unsafe_allow_html=True,
)
