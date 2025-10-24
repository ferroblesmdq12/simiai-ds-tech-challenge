-- ================================================
-- Creamos la Base de Datos 'partnersdb' - SimiAI
-- ================================================
CREATE DATABASE partnersdb
WITH 
    OWNER = postgres
    ENCODING = 'UTF8'
    LC_COLLATE = 'Spanish_Argentina.1252'
    LC_CTYPE = 'Spanish_Argentina.1252'
    TABLESPACE = pg_default
    CONNECTION LIMIT = -1;

-- ======================================
-- SCHEMA: Sistema de Partners - SimiAI
-- ======================================

-- 1. Tabla de países
CREATE TABLE countries (
    id_country SERIAL PRIMARY KEY,
    country_name VARCHAR(50) NOT NULL
);

-- 2. Tabla de planes comerciales
CREATE TABLE plans (
    id_plan SERIAL PRIMARY KEY,
    plan_name VARCHAR(50) NOT NULL,
    monthly_fee NUMERIC(10,2),
    notification_limit INT
);

-- 3. Tabla de estados
CREATE TABLE statuses (
    id_status SERIAL PRIMARY KEY,
    status_name VARCHAR(30) NOT NULL
);

-- 4. Tabla principal: partners
CREATE TABLE partners (
    id_partner SERIAL PRIMARY KEY,
    partner_name VARCHAR(100) NOT NULL,
    country_id INT REFERENCES countries(id_country),
    plan_id INT REFERENCES plans(id_plan),
    status_id INT REFERENCES statuses(id_status),
    join_date DATE NOT NULL DEFAULT CURRENT_DATE
);

-- 5. Tabla de notificaciones enviadas por cada partner
CREATE TABLE notifications (
    id_notification SERIAL PRIMARY KEY,
    partner_id INT REFERENCES partners(id_partner),
    notification_date DATE NOT NULL,
    notification_count INT CHECK (notification_count >= 0)
);

SELECT * FROM statuses;
SELECT * FROM plans;
SELECT * FROM countries;
SELECT * FROM notifications;
SELECT * FROM partners;

