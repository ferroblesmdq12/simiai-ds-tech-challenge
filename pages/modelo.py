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

def show():
    st.title("🧠 Modelo de Machine Learning - Predicción de Churn")

    model_path = r"C:\Users\Fernando\Desktop\Reto Técnico SimiAI\ml\modelo_churn.joblib"
    csv_path = r"C:\Users\Fernando\Desktop\Reto Técnico SimiAI\ml\churn_results.csv"

    if not os.path.exists(model_path) or not os.path.exists(csv_path):
        st.error("⚠️ No se encontraron los archivos del modelo o los resultados. Ejecutá el notebook primero.")
        return

    # Cargar modelo y datos
    model = joblib.load(model_path)
    df = pd.read_csv(csv_path)

    st.markdown("### 🧩 Detalles del modelo entrenado")
    st.write(model)

    # Mostrar métricas básicas
    st.subheader("📊 Distribución de predicciones")
    fig = px.histogram(df, x="prob_churn", nbins=25, title="Distribución de probabilidades de churn")
    st.plotly_chart(fig)

    # Feature importances (solo si el modelo tiene atributo)
    if hasattr(model, "feature_importances_"):
        st.subheader("🔥 Importancia de variables")
        importances = pd.Series(model.feature_importances_, index=model.feature_names_in_)
        importances = importances.sort_values(ascending=True)
        fig_imp = px.bar(importances, orientation='h', title="Importancia de características")
        st.plotly_chart(fig_imp)
    else:
        st.info("El modelo no posee atributo de importancia de variables (no es un árbol o ensemble).")

    st.markdown("---")
    st.markdown("<p style='text-align:center; color:gray;'>© 2025 SimiAI | Desarrollado por Fernando Raúl Robles</p>", unsafe_allow_html=True)
