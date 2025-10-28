# 🚀 Sistema de Partners — SimiAI

**Autor:** Fernando Raúl Robles  
**Tecnologías:** Python | Streamlit | PostgreSQL | Plotly | Pandas  
**Base de datos:** Neon.tech (PostgreSQL Cloud)  
**Dashboard Online:** 👉 [Ver aplicación en Streamlit Cloud](https://dashboard-simiai.streamlit.app/)

---

## 🧠 Descripción General

El **Sistema de Partners — SimiAI** es un módulo analítico diseñado para centralizar, monitorear y visualizar información sobre los **partners comerciales** de una organización.

El sistema integra datos de países, planes, estados y notificaciones, generando **KPIs interactivos** mediante un **dashboard en Streamlit**, conectado a una base de datos **PostgreSQL en la nube (Neon.tech)**.

---

## 🧩 Objetivos del Proyecto

- Centralizar la información de partners y sus relaciones.
- Evaluar desempeño comercial mediante **KPIs y métricas interactivas**.
- Analizar la distribución geográfica y la evolución temporal de altas.
- Visualizar actividad y engagement de los partners mediante **notificaciones**.

---

## 🏗️ Arquitectura del Sistema

El proyecto está compuesto por tres capas principales:

1. **Capa de Datos (PostgreSQL / Neon.tech)**
   - Tablas: `countries`, `plans`, `statuses`, `partners`, `notifications`
   - Relaciones definidas mediante claves foráneas (ver diagrama ERD).

2. **Capa de Análisis (Python + Pandas)**
   - Limpieza y merge de datos para análisis de KPIs.
   - Cálculo de métricas clave: partners activos, notificaciones promedio, distribución por país, etc.

3. **Capa de Visualización (Streamlit + Plotly)**
   - Dashboard interactivo con filtros por país, plan y fecha.
   - Gráficos dinámicos: barras, líneas, tortas y tarjetas de resumen.

---

## 📊 Diagrama Entidad–Relación

![ERD_SimiAI_PartnersDB](reports/Diagrama%20Entidad%20Relación.PNG)

> El modelo relacional respeta la normalización 3NF, garantizando integridad referencial y consistencia de los datos.

---

## 📁 Estructura del Proyecto

RETO TÉCNICO SIMIAI/
│
├── .devcontainer/ # Configuración para contenedor remoto (Codespaces / Docker)
│ └── devcontainer.json
│
├── sql/ # Scripts SQL
│ ├── partners_schema.sql # Definición del esquema de base de datos
│ ├── data_load.sql # Inserción de datos simulados
│ └── queries_kpis.sql # Consultas de análisis y KPIs
│
├── src/ # Código fuente del dashboard
│ └── streamlit_app.py
│
├── reports/ # Diagramas e informes
│ ├── Diagrama Entidad Relación.PNG
│ ├── ERD_SimiAI_PartnersDB.pdf
│ └── ColorsPalette.PNG
│
├── requirements.txt # Dependencias del proyecto
└── README.md # Documentación general


---

## ⚙️ Configuración del Entorno

### 🧩 Requisitos Previos

- Python 3.11+
- PostgreSQL (o una cuenta en [Neon.tech](https://neon.tech))
- Git y Visual Studio Code  
  *(opcional: soporte para Dev Containers o GitHub Codespaces)*

---

### 🚀 Instalación y Ejecución Local

```bash
# 1️⃣ Clonar el repositorio
git clone https://github.com/ferroblesmdq12/simiai-ds-tech-challenge.git

# 2️⃣ Entrar al directorio del proyecto
cd simiai-ds-tech-challenge

# 3️⃣ Instalar dependencias
pip install -r requirements.txt

# 4️⃣ Ejecutar el dashboard de Streamlit
streamlit run src/streamlit_app.py

# 
###  KPI

| KPI                                     | Descripción                                                                |
| --------------------------------------- | -------------------------------------------------------------------------- |
| **Partners Activos por Plan**           | Muestra cuántos partners están activos según el plan comercial contratado. |
| **Evolución de Altas Mensuales**        | Representa la tendencia de altas de nuevos partners por mes.               |
| **Distribución Geográfica**             | Indica la cantidad de partners por país (gráfico horizontal).              |
| **Promedio de Notificaciones por Plan** | Mide la actividad promedio de comunicación por plan.                       |
| **Top 10 Partners por Notificaciones**  | Identifica los partners más activos en el sistema.                         |


###🎨 Paleta de Colores

La paleta azul se diseñó para optimizar la visualización en modo oscuro y mantener coherencia con el estilo del dashboard.


### 🧱 Dev Container (Entorno Reproducible)

El archivo devcontainer.json
 configura un entorno reproducible basado en Python 3.11 (Bookworm).
Al abrir el proyecto en VS Code o GitHub Codespaces:

Instala automáticamente todas las dependencias (requirements.txt)

Ejecuta el comando streamlit run src/streamlit_app.py

Abre los archivos principales (README.md, streamlit_app.py)

Expone el puerto 8501 con vista previa del dashboard

Esto garantiza que el proyecto funcione igual en cualquier entorno local o remoto 🐳




## 👨‍💻 Autor

Fernando Raúl Robles

📊 Data Analyst | Python | SQL | Power BI | BigQuery | Google Cloud | Visualization | KPIs | ETL | AI Automation | n8n | Streamlit | Neon 

🌐 Portfolio Web: https://ferroblesmdq12.github.io/myprofile/?lang=en

💼 LinkedIn: https://www.linkedin.com/in/fernando-ra%C3%BAl-robles-bbb214223/

📧 fernando.robles.mdq@gmail.com