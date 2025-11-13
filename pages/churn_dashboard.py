# ============================================================
# 📊 CHURN DASHBOARD - Proyecto SimiAI
# Autor: Fernando Raúl Robles
# Fecha: 05/11/2025
# Descripción:
# Visualización simple de resultados de churn
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
    "Dashboard de análisis del modelo **Random Forest** encargado de estimar la probabilidad de baja de cada partner."
)
st.markdown("---")

# ------------------------------------------------------------
# RUTAS DE ARCHIVOS
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
        st.warning(f"⚠️ No se pudo cargar el modelo. Se continuará solo con los datos.\n\n**Detalle:** {e}")
else:
    st.info("ℹ️ No se encontró el archivo `modelo_churn.joblib`.")

# ------------------------------------------------------------
# CARGA DEL CSV CON RESULTADOS
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
# RENOMBRADO PROFESIONAL DE COLUMNAS
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

tasa_baja = df["churn"].mean()
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
# TOP 10 PARTNERS CON MAYOR RIESGO
# ------------------------------------------------------------
st.subheader("⚠️ Top 10 Partners con mayor probabilidad de baja")

top_riesgo = df.sort_values("Probabilidad de baja", ascending=False).head(10)

st.dataframe(
    top_riesgo[["Partner", "Plan", "Estado", "Probabilidad de baja"]],
    use_container_width=True,
)

# ------------------------------------------------------------
# PROMEDIO DE BAJAS POR PLAN
# ------------------------------------------------------------
st.subheader("📊 Probabilidad promedio de baja por plan")

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
    color_discrete_sequence=["#4f9bee"]
)
st.plotly_chart(fig2, use_container_width=True)

# ------------------------------------------------------------
# IMPORTANCIA DE VARIABLES (si disponible)
# ------------------------------------------------------------
if model is not None and hasattr(model, "feature_importances_"):
    st.subheader("🧩 Importancia de Variables en el Modelo")

    importancias = pd.Series(model.feature_importances_, index=model.feature_names_in_)
    importancias = importancias.sort_values(ascending=True)

    fig_imp = px.bar(
        importancias,
        orientation="h",
        title="Importancia de características",
        labels={"value": "Importancia", "index": "Variable"},
        color_discrete_sequence=["#4f9bee"],
    )
