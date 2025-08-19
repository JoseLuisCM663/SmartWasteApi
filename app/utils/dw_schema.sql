-- ====================================================
-- SmartWaste Data Warehouse Schema (Estrella)
-- ====================================================

-- ==============================================
-- Dimensiones
-- ==============================================

-- Dimensión de sensores
CREATE TABLE  IF NOT EXISTS Dim_Sensor (
    Sensor_ID INT PRIMARY KEY,
    Contenedor_ID INT,
    Tipo VARCHAR(50),
    Ubicacion VARCHAR(100)
);

-- Dimensión de contenedores
CREATE TABLE  IF NOT EXISTS Dim_Contenedor (
    Contenedor_ID INT PRIMARY KEY,
    Ruta_ID INT,
    Capacidad INT,
    Ubicacion VARCHAR(100)

);

-- Dimensión de rutas
CREATE TABLE  IF NOT EXISTS Dim_Ruta (
    Ruta_ID INT PRIMARY KEY,
    Nombre_Ruta VARCHAR(50),
    Estatus BOOLEAN DEFAULT TRUE
);

-- Dimensión de usuarios
CREATE TABLE  IF NOT EXISTS Dim_Usuario (
    Usuario_ID INT PRIMARY KEY,
    Nombre VARCHAR(100),
    Rol VARCHAR(50)
);

-- Dimensión de tiempo
CREATE TABLE IF NOT EXISTS Dim_Tiempo (
    Tiempo_ID INT PRIMARY KEY,
    Fecha DATE,
    Hora INT,
    DiaSemana VARCHAR(10),
    Mes INT,
    Año INT
);

-- ==============================================
-- Tabla de hechos
-- ==============================================

CREATE TABLE  IF NOT EXISTS Fact_Lecturas (
    Lectura_ID INT PRIMARY KEY,
    Sensor_ID INT,
    Contenedor_ID INT,
    Ruta_ID INT,
    Tiempo_ID INT,
    Valor FLOAT,
    FOREIGN KEY (Sensor_ID) REFERENCES Dim_Sensor(Sensor_ID),
    FOREIGN KEY (Contenedor_ID) REFERENCES Dim_Contenedor(Contenedor_ID),
    FOREIGN KEY (Ruta_ID) REFERENCES Dim_Ruta(Ruta_ID),
    FOREIGN KEY (Tiempo_ID) REFERENCES Dim_Tiempo(Tiempo_ID)
);



