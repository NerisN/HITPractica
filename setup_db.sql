-- Script de configuración inicial de la base de datos
-- Ejecutar: psql -U postgres -f setup_db.sql

CREATE DATABASE co2_monitoreo;
\c co2_monitoreo;

CREATE TABLE lecturas (
    id SERIAL PRIMARY KEY,
    co2_ppm FLOAT NOT NULL,
    temperatura FLOAT NOT NULL,
    laboratorio VARCHAR(100) DEFAULT 'Lab-Sw-01',
    nivel_alerta VARCHAR(20) DEFAULT 'NORMAL',
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_timestamp ON lecturas(timestamp DESC);
CREATE INDEX idx_nivel_alerta ON lecturas(nivel_alerta);
CREATE INDEX idx_laboratorio ON lecturas(laboratorio);

-- Inserto inicial de datos de prueba
INSERT INTO lecturas (co2_ppm, temperatura, laboratorio, nivel_alerta) VALUES
(612.0, 22.1, 'Lab-Sw-01', 'NORMAL'),
(891.0, 24.3, 'Lab-Sw-01', 'MODERADO'),
(1248.0, 26.8, 'Lab-Sw-01', 'ALTO'),
(1731.0, 28.5, 'Lab-Sw-01', 'CRÍTICO');

SELECT COUNT(*) as total_registros FROM lecturas;
