# ============================================================
# MODELO ML - Proyecto SimiAI
# Autor: Fernando Raúl Robles
# Fecha: 05/11/2025
# Descripción:
# Visualización y análisis del modelo de Machine Learning
# ============================================================

import streamlit as st
import pandas as pd
import joblib
import plotly.express as px
import os

# Config inicial (opcional)
st.set_page_config(page_title="Modelo ML - SimiAI", page_icon="🧠", layout="wide")

st.title("🧠 Modelo de Machine Learning - Predicción de Churn")
st.markdown("Exploración del modelo RandomForest entrenado sobre la base de datos de Partners SimiAI.")

# -----------------------------------------------
# Rutas absolutas (ajustadas a tu entorno)
# -----------------------------------------------
model_path = r"C:\Users\Fernando\Desktop\Reto Técnico SimiAI\ml\modelo_churn.joblib"
csv_path = r"C:\Users\Fernando\Desktop\Reto Técnico SimiAI\ml\churn_results.csv"

if not os.path.exists(model_path) or not os.path.exists(csv_path):
    st.error("⚠️ No se encontraron los archivos del modelo o los resultados. Ejecutá el notebook primero.")
    st.stop()

# -----------------------------------------------
# Cargar modelo y datos
# -----------------------------------------------
model = joblib.load(model_path)
df = pd.read_csv(csv_path)

st.success("✅ Modelo y datos cargados correctamente.")

# -----------------------------------------------
# Información del modelo
# -----------------------------------------------
st.markdown("### 🧩 Detalles del modelo entrenado")
st.write(model)

# -----------------------------------------------
# Visualización: Distribución de probabilidades
# -----------------------------------------------
st.subheader("📊 Distribución de predicciones")
fig = px.histogram(df, x="prob_churn", nbins=25,
                   title="Distribución de probabilidades de churn",
                   color_discrete_sequence=["#4f9bee"])
st.plotly_chart(fig, use_container_width=True)

# -----------------------------------------------
# Importancia de variables
# -----------------------------------------------
if hasattr(model, "feature_importances_"):
    st.subheader("🔥 Importancia de variables (Feature Importance)")
    importances = pd.Series(model.feature_importances_, index=model.feature_names_in_)
    importances = importances.sort_values(ascending=True)
    fig_imp = px.bar(importances, orientation='h', title="Importancia de características",
                     color_discrete_sequence=["#4f9bee"])
    st.plotly_chart(fig_imp, use_container_width=True)
else:
    st.info("ℹ️ Este modelo no posee información de importancia de variables (no es un árbol o ensemble).")

# -----------------------------------------------
# Pie de página
# -----------------------------------------------
st.markdown("---")
st.markdown("<p style='text-align:center; color:gray;'>© 2025 SimiAI | Desarrollado por Fernando Raúl Robles</p>", unsafe_allow_html=True)
