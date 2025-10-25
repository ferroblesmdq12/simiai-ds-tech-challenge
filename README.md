
# Sistema de Partners — Reto Técnico SimiAI (ds-tech-challenge)

## 📘 Descripción General
El sistema de Partners centraliza información de empresas asociadas que colaboran o distribuyen servicios de SimiAI. 
Permite analizar su desempeño, actividad y evolución temporal a través de KPIs y dashboards analíticos.

## 🧱 Modelo de Datos
- **countries**: países de operación (LATAM)
- **plans**: planes comerciales (Basic, Standard, Premium, Enterprise)
- **statuses**: estado operativo del partner
- **partners**: entidad principal con referencias a país, plan y estado
- **notifications**: registros de actividad y notificaciones enviadas

## ⚙️ Instrucciones de instalación
1. Crear base de datos `partnersdb`
2. Ejecutar `partners_schema.sql`
3. Ejecutar `data_load.sql`
4. Ejecutar `queries_kpis.sql` para análisis

## 📊 Próximos pasos
- Incorporar KPIs avanzados (retención, churn, ingresos estimados)
- Crear dashboard analítico (Power BI / Jupyter Notebook)
- Documentar resultados e interpretaciones
