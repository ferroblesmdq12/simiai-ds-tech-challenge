# ============================================================
# 📊 CHURN DASHBOARD - Proyecto SimiAI
# Autor: Fernando Raúl Robles
# Fecha: 05/11/2025
# Descripción:
# Visualización de resultados del modelo de churn
# entrenado en ml/churn_model.ipynb
# ============================================================

import streamlit as st
import pandas as pd
import plotly.express as px
import os

def show():
    st.title("📉 Análisis de Churn - Partners en Riesgo")
    st.markdown("Este módulo muestra los resultados del modelo de *machine learning* entrenado en Python sobre la base de datos de SimiAI.")

    # Ruta del archivo generado por el modelo
    path_csv = path_csv = os.path.join("ml", "churn_results.csv")


    if not os.path.exists(path_csv):
        st.error("⚠️ No se encontró el archivo 'churn_results.csv'. Ejecutá primero el notebook de entrenamiento.")
        return

    # Cargar datos
    df = pd.read_csv(path_csv)

    # KPIs principales
    col1, col2, col3 = st.columns(3)
    churn_rate = df["churn"].mean()
    avg_prob = df["probabilidad de churn"].mean()
    total_partners = len(df)

    col1.metric("Total de Partners", f"{total_partners}")
    col2.metric("Tasa de Churn Real", f"{churn_rate:.2%}")
    col3.metric("Probabilidad Promedio de Churn", f"{avg_prob:.2%}")

    # Histograma de probabilidad
    st.subheader("Distribución de probabilidad de churn")
    fig = px.histogram(df, x="prob_churn", nbins=25,
                       title="Distribución de probabilidad de churn",
                       color_discrete_sequence=["#ff6666"])
    st.plotly_chart(fig, use_container_width=True)

    # Top 10 partners en riesgo
    st.subheader("Top 10 Partners con mayor probabilidad de churn")
    risky = df.sort_values("prob_churn", ascending=False).head(10)
    st.dataframe(risky[["partner_name", "plan_name", "status_name", "prob_churn"]])

    # Churn por plan
    st.subheader("Tasa promedio de churn por plan")
    churn_plan = df.groupby("plan_name")["prob_churn"].mean().reset_index()
    fig2 = px.bar(churn_plan, x="Plan", y="probabilidad de churn",
                  title="Promedio de churn por plan",
                  text_auto=".2%",
                  color="plan_name")
    st.plotly_chart(fig2, use_container_width=True)

# Ejecutar la función automáticamente al cargar la página
if __name__ == "__main__":
    show()
else:
    show()