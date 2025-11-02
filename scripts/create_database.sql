-- Script para crear la base de datos y tabla en SQL Server

-- Crear base de datos
USE master;
GO
IF NOT EXISTS (SELECT * FROM sys.databases WHERE name = 'BancoDB')
BEGIN
    CREATE DATABASE BancoDB;
END
GO

USE BancoDB;
GO

-- Crear tabla de transacciones procesadas
CREATE TABLE transacciones_clientes (
        id_transaccion VARCHAR(50) PRIMARY KEY,
        id_cliente VARCHAR(50),
        id_cuenta VARCHAR(50),
        fecha DATE,
        tipo_transaccion VARCHAR(50),
        monto FLOAT,
        canal VARCHAR(50),
        monto_usd FLOAT,
        nombre VARCHAR(100),
        ciudad VARCHAR(50),
        email VARCHAR(100),
        ingreso_mensual FLOAT,
        ingreso_mensual_usd FLOAT,
        ingreso_anual FLOAT,
        ingreso_anual_usd FLOAT,
        riesgo_crediticio VARCHAR(50),
        tipo_cuenta VARCHAR(50),
        estado_cuenta VARCHAR(50),
        saldo FLOAT,
        saldo_usd FLOAT,
    );
GO

-- Consultas útiles para validar los datos
-- SELECT COUNT(*) as total_registros FROM transacciones_clientes;
-- SELECT SUM(monto) as monto_total_pen, SUM(monto_usd) as monto_total_usd FROM transacciones_clientes;
-- SELECT tipo_transaccion, COUNT(*) as cantidad, SUM(monto) as monto_total FROM transacciones_clientes GROUP BY tipo_transaccion;
