# 🚀 Sistema de Partners  

**Autor:** Fernando Raúl Robles  
**Tecnologías:** Python | Streamlit | PostgreSQL | Plotly | Pandas | Scikit-Learn  
**Base de datos:** Neon.tech (PostgreSQL Cloud)  
**Dashboard Online:** 👉 [Ver aplicación en Streamlit Cloud](https://dashboard-simiai.streamlit.app/)  

---

## 🧠 Descripción General

El **Sistema de Partners — SimiAI** es una plataforma analítica completa diseñada para **centralizar, monitorear y visualizar** la información clave de los partners comerciales de una organización.

Incluye:

- Dashboard ejecutivo con KPIs, mapas, líneas de tiempo y análisis por plan/industria.
- Panel operativo con distribución geográfica, actividad y notificaciones.
- **Modelo de Machine Learning** para predecir la **probabilidad de baja (churn)**.
- Integración en tiempo real con base de datos **PostgreSQL (Neon.tech)**.
- Visualizaciones interactivas en **modo oscuro** con estilo profesional.

El proyecto combina **Data Analytics + Data Engineering + Machine Learning + Visualización Avanzada**.

---

## 🧩 Objetivos del Proyecto

- Centralizar la información de partners en una base consistente y normalizada.
- Evaluar desempeño comercial mediante **KPIs interactivos**.
- Analizar **distribución geográfica**, planes comerciales e industrias.
- Visualizar actividad y engagement mediante **notificaciones**.
- Detectar **riesgo de baja** mediante un modelo de ML.
- Obtener insights ejecutivos generados automáticamente.
- Facilitar toma de decisiones basada en datos para el equipo comercial.

---

## 🏗️ Arquitectura del Sistema

El proyecto implementa un flujo completo:

### 🔹 1. Capa de Datos (PostgreSQL / Neon.tech)
- Tablas: `countries`, `plans`, `statuses`, `partners`, `notifications`.
- Modelo totalmente normalizado (3NF).
- Conexión segura administrada con reconexión automática.
- Carga modular desde `src/data_loader.py`.

### 🔹 2. Capa de Análisis (Python + Pandas)
- Limpieza y merge de tablas.
- Generación de KPIs ejecutivos.
- Agrupaciones temporales (evolución por mes).
- Identificación de tendencias y oportunidades.

### 🔹 3. Capa de Visualización (Streamlit + Plotly)
- Dashboard interactivo con filtros combinables.
- Modo oscuro custom.
- Insights narrados automáticos.
- Páginas múltiples (Dashboard + Modelo ML).

### 🔹 4. Capa de Machine Learning (Scikit-Learn)
- Entrenamiento de modelo **Random Forest**.
- Exportación con `joblib`.
- Generación del dataset predicho: `ml/churn_results.csv`.
- Página dedicada a predicción de bajas en `/pages/modelo.py`.

---

## 📊 Dashboard Principal – Funcionalidades

El dashboard incluye:

### ✔ KPIs ejecutivos
