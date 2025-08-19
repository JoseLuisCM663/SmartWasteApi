# app/utils/etl/dw_etl.py
from app.database import engine
import pandas as pd
from sqlalchemy import text

# ==============================
# Funciones para cargar Dimensiones
# ==============================

def cargar_dim_sensor():
    """Dimensión Sensores"""
    try:
        query = """
            SELECT 
                s.ID AS Sensor_ID,
                s.Contenedor_Id AS Contenedor_ID,
                s.Tipo,
                c.Ubicacion
            FROM tbb_sensores s
            JOIN tbb_contenedores c ON s.Contenedor_Id = c.ID
        """
        df = pd.read_sql(query, engine)
        df = df[["Sensor_ID", "Contenedor_ID", "Tipo", "Ubicacion"]]
        df = df.drop_duplicates(subset=["Sensor_ID"])
        
        # Insertar con manejo de duplicados
        insert_stmt = """
        INSERT INTO dim_sensor (Sensor_ID, Contenedor_ID, Tipo, Ubicacion)
        VALUES (:Sensor_ID, :Contenedor_ID, :Tipo, :Ubicacion)
        ON DUPLICATE KEY UPDATE
            Contenedor_ID = VALUES(Contenedor_ID),
            Tipo = VALUES(Tipo),
            Ubicacion = VALUES(Ubicacion)
        """
        with engine.begin() as conn:
            conn.execute(text(insert_stmt), df.to_dict(orient="records"))
        print("✅ Dimensión Dim_Sensor cargada sin duplicados.")
    except Exception as e:
        print(f"❌ Error al cargar Dim_Sensor: {e}")


def cargar_dim_contenedor():
    """Dimensión Contenedores"""
    try:
        query = """
            SELECT ID AS Contenedor_ID,
                   Ubicacion,
                   Capacidad,
                   Ruta_Id
            FROM tbb_contenedores
        """
        df = pd.read_sql(query, engine)
        df = df.drop_duplicates(subset=["Contenedor_ID"])

        insert_stmt = """
        INSERT INTO dim_contenedor (Contenedor_ID, Ubicacion, Capacidad, Ruta_Id)
        VALUES (:Contenedor_ID, :Ubicacion, :Capacidad, :Ruta_Id)
        ON DUPLICATE KEY UPDATE
            Ubicacion = VALUES(Ubicacion),
            Capacidad = VALUES(Capacidad),
            Ruta_Id = VALUES(Ruta_Id)
        """
        with engine.begin() as conn:
            conn.execute(text(insert_stmt), df.to_dict(orient="records"))
        print("✅ Dimensión Dim_Contenedor cargada sin duplicados.")
    except Exception as e:
        print(f"❌ Error al cargar Dim_Contenedor: {e}")


def cargar_dim_ruta():
    """Dimensión Rutas"""
    try:
        query = """
            SELECT ID AS Ruta_ID,
                   Nombre AS Nombre_Ruta,
                   Estatus
            FROM tbb_rutas_recoleccion
        """
        df = pd.read_sql(query, engine)
        df = df.drop_duplicates(subset=["Ruta_ID"])

        insert_stmt = """
        INSERT INTO dim_ruta (Ruta_ID, Nombre_Ruta, Estatus)
        VALUES (:Ruta_ID, :Nombre_Ruta, :Estatus)
        ON DUPLICATE KEY UPDATE
            Nombre_Ruta = VALUES(Nombre_Ruta),
            Estatus = VALUES(Estatus)
        """
        with engine.begin() as conn:
            conn.execute(text(insert_stmt), df.to_dict(orient="records"))
        print("✅ Dimensión Dim_Ruta cargada sin duplicados.")
    except Exception as e:
        print(f"❌ Error al cargar Dim_Ruta: {e}")


def cargar_dim_usuario():
    """Dimensión Usuarios"""
    try:
        query = """
            SELECT ID AS Usuario_ID,
                   Nombre_Usuario AS Nombre,
                   Tipo_Usuario AS Rol
            FROM tbb_usuarios
        """
        df = pd.read_sql(query, engine)
        df = df.drop_duplicates(subset=["Usuario_ID"])

        insert_stmt = """
        INSERT INTO dim_usuario (Usuario_ID, Nombre, Rol)
        VALUES (:Usuario_ID, :Nombre, :Rol)
        ON DUPLICATE KEY UPDATE
            Nombre = VALUES(Nombre),
            Rol = VALUES(Rol)
        """
        with engine.begin() as conn:
            conn.execute(text(insert_stmt), df.to_dict(orient="records"))
        print("✅ Dimensión Dim_Usuario cargada sin duplicados.")
    except Exception as e:
        print(f"❌ Error al cargar Dim_Usuario: {e}")


def cargar_dim_tiempo():
    """Dimensión Tiempo"""
    try:
        query = """
            SELECT DISTINCT
                   DATE(Fecha) AS Fecha,
                   HOUR(Fecha) AS Hora,
                   DAYNAME(Fecha) AS DiaSemana,
                   MONTH(Fecha) AS Mes,
                   YEAR(Fecha) AS Año
            FROM tbd_lecturas_sensores
        """
        df = pd.read_sql(query, engine)
        df = df.reset_index(drop=True)
        df["Tiempo_ID"] = df.index + 1
        df = df[["Tiempo_ID", "Fecha", "Hora", "DiaSemana", "Mes", "Año"]]

        insert_stmt = """
        INSERT INTO dim_tiempo (Tiempo_ID, Fecha, Hora, DiaSemana, Mes, Año)
        VALUES (:Tiempo_ID, :Fecha, :Hora, :DiaSemana, :Mes, :Año)
        ON DUPLICATE KEY UPDATE
            Fecha = VALUES(Fecha),
            Hora = VALUES(Hora),
            DiaSemana = VALUES(DiaSemana),
            Mes = VALUES(Mes),
            Año = VALUES(Año)
        """
        with engine.begin() as conn:
            conn.execute(text(insert_stmt), df.to_dict(orient="records"))
        print("✅ Dimensión Dim_Tiempo cargada sin duplicados.")
    except Exception as e:
        print(f"❌ Error al cargar Dim_Tiempo: {e}")


def cargar_fact_lecturas():
    """
    Tabla de hechos: lecturas de sensores
    Se asegura que cada lectura tenga un Tiempo_ID válido en Dim_Tiempo.
    """
    try:
        # Cargar lecturas
        query_lecturas = """
            SELECT l.ID AS Lectura_ID,
                   l.Valor,
                   l.Fecha,
                   l.Sensor_Id,
                   s.Contenedor_Id,
                   c.Ruta_Id
            FROM tbd_lecturas_sensores l
            JOIN tbb_sensores s ON l.Sensor_Id = s.ID
            JOIN tbb_contenedores c ON s.Contenedor_Id = c.ID
        """
        df = pd.read_sql(query_lecturas, engine)

        # Convertir Fecha a datetime
        df['Fecha'] = pd.to_datetime(df['Fecha'])
        df['Hora'] = df['Fecha'].dt.hour

        # Cargar Dim_Tiempo existente
        df_tiempo = pd.read_sql("SELECT * FROM dim_tiempo", engine)
        df_tiempo['Fecha'] = pd.to_datetime(df_tiempo['Fecha'])
        df_tiempo['Hora'] = df_tiempo['Hora'].astype(int)

        # Identificar fechas/hours de lecturas que no existen en Dim_Tiempo
        df_merge = df.merge(df_tiempo[['Tiempo_ID', 'Fecha', 'Hora']],
                            on=['Fecha', 'Hora'], how='left', indicator=True)

        # Filas sin Tiempo_ID
        df_faltantes = df_merge[df_merge['_merge'] == 'left_only'][['Fecha', 'Hora']].drop_duplicates()

        if not df_faltantes.empty:
            print("⚠️ Creando Tiempo_ID faltantes en Dim_Tiempo...")
            # Asignar nuevos IDs incrementales
            max_id = df_tiempo['Tiempo_ID'].max() if not df_tiempo.empty else 0
            df_faltantes['Tiempo_ID'] = range(max_id + 1, max_id + 1 + len(df_faltantes))

            # Insertar nuevos registros en Dim_Tiempo
            insert_stmt = """
                INSERT INTO dim_tiempo (Tiempo_ID, Fecha, Hora)
                VALUES (:Tiempo_ID, :Fecha, :Hora)
            """
            records = df_faltantes.to_dict(orient='records')
            with engine.begin() as conn:
                conn.execute(text(insert_stmt), records)
            
            # Actualizar df_tiempo con los nuevos registros
            df_tiempo = pd.concat([df_tiempo, df_faltantes], ignore_index=True)

        # Hacer merge final para obtener Tiempo_ID completo
        df = df.merge(df_tiempo[['Tiempo_ID', 'Fecha', 'Hora']],
                      how='left', on=['Fecha', 'Hora'])

        # Seleccionar columnas de la tabla de hechos
        df_fact = df[['Lectura_ID', 'Sensor_Id', 'Contenedor_Id', 'Ruta_Id', 'Tiempo_ID', 'Valor']]

        # Insertar usando ON DUPLICATE KEY UPDATE
        insert_stmt = """
            INSERT INTO fact_lecturas (Lectura_ID, Sensor_Id, Contenedor_Id, Ruta_Id, Tiempo_ID, Valor)
            VALUES (:Lectura_ID, :Sensor_Id, :Contenedor_Id, :Ruta_Id, :Tiempo_ID, :Valor)
            ON DUPLICATE KEY UPDATE
                Valor = VALUES(Valor)
        """
        records = df_fact.to_dict(orient='records')
        with engine.begin() as conn:
            conn.execute(text(insert_stmt), records)

        print("✅ Tabla de hechos Fact_Lecturas cargada correctamente.")
    
    except Exception as e:
        print(f"❌ Error al cargar Fact_Lecturas: {e}")


def ejecutar_etl():
    """Ejecuta todas las funciones ETL en orden correcto"""
    cargar_dim_ruta()
    cargar_dim_contenedor()
    cargar_dim_sensor()
    cargar_dim_usuario()
    cargar_dim_tiempo()
    cargar_fact_lecturas()
    print("✅ ETL completo. Data Warehouse actualizado.")
