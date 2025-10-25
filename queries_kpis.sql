-- =====================================================================================
-- Consultas analíticas (KPIs) - Sistema de Partners (Reto SimiAI)
-- =====================================================================================
-- Autor: Fernando Raúl Robles
-- Fecha: 25/10/2025
-- Descripción:
-- Este script se generan consultas SQL en la base partnersdb, para extraer los datos y 
-- transformarlo en información valiosa para el negocio.
-- =====================================================================================

-- ============================================
-- KPI 1 - Partners activos por tipo de plan.
-- ============================================

SELECT 
    p.plan_name,
    COUNT(pa.id_partner) AS active_partners
FROM partners pa
JOIN plans p ON pa.plan_id = p.id_plan
JOIN statuses s ON pa.status_id = s.id_status
WHERE s.status_name = 'Activo'
GROUP BY p.plan_name
ORDER BY active_partners DESC;

-- ================================================
-- KPI 2 - Evolucion temporal de altas de partners.
-- ================================================

SELECT 
    TO_CHAR(join_date, 'YYYY-MM') AS month,
    COUNT(id_partner) AS partners_added
FROM partners
GROUP BY TO_CHAR(join_date, 'YYYY-MM')
ORDER BY month;


-- ================================================
-- KPI 3 - Distribución de partners por país.
-- ================================================

SELECT 
    c.country_name,
    COUNT(pa.id_partner) AS total_partners
FROM partners pa
JOIN countries c ON pa.country_id = c.id_country
GROUP BY c.country_name
ORDER BY total_partners DESC;


-- ====================================================
-- KPI 4 - Total y promedio de notificaciones por plan.
-- ====================================================

SELECT 
    pl.plan_name,
    COUNT(n.id_notification) AS total_notifications,
    ROUND(AVG(n.notification_count), 2) AS avg_notifications
FROM notifications n
JOIN partners pa ON n.partner_id = pa.id_partner
JOIN plans pl ON pa.plan_id = pl.id_plan
GROUP BY pl.plan_name
ORDER BY avg_notifications DESC;

-- ==========================================================================
-- KPI 5 - Ratio de actividad (partners con notificaciones / total partners).
-- ==========================================================================

SELECT 
    ROUND(
        (COUNT(DISTINCT n.partner_id)::decimal / COUNT(DISTINCT pa.id_partner)) * 100, 2
    ) AS active_ratio_percentage
FROM partners pa
LEFT JOIN notifications n ON pa.id_partner = n.partner_id;


-- =============================================================
-- KPI 6 - Top 10 partners por volumen total de notificaciones
-- =============================================================

SELECT 
    pa.partner_name,
    SUM(n.notification_count) AS total_notifications
FROM notifications n
JOIN partners pa ON n.partner_id = pa.id_partner
GROUP BY pa.partner_name
ORDER BY total_notifications DESC
LIMIT 10;

