import pandas as pd
from sqlalchemy.orm import Session
from app.models.lectura_sensor import LecturaSensor
import numpy as np
from app.models.bitacora_recolecion import BitacoraRecoleccion
from app.models.bitacora_contenedor import BitacoraContenedor


def exportar_todas_lecturas(ruta_csv: str, db: Session):
    """
    ETL completo de lecturas de TODOS los sensores:
    - Extrae de la BD
    - Transforma: limpieza, interpolación, resampleo por sensor, features
    - Carga a CSV
    """

    try:
        # 1) EXTRACCIÓN
        lecturas = db.query(LecturaSensor).all()

        # Convertir a DataFrame
        data = [{
            "ID": l.ID,
            "Sensor_Id": l.Sensor_Id,
            "Valor": l.Valor,
            "Fecha": l.Fecha,
        } for l in lecturas]

        df = pd.DataFrame(data)

        if df.empty:
            print("No hay lecturas para exportar.")
            return

        # 2) TRANSFORMACIÓN Y LIMPIEZA
        df["Fecha"] = pd.to_datetime(df["Fecha"])
        df = df.sort_values(["Sensor_Id", "Fecha"])
        df = df.drop_duplicates(subset=["ID"], keep="first")
        df = df[df["Valor"].notna()]
        df["Valor"] = df["Valor"].clip(lower=0, upper=100)
        df = df.set_index("Fecha")

        # Resampleo e interpolación por sensor sin warnings
        resampled_list = []

        for sensor_id, g in df.groupby("Sensor_Id"):
            g_resampled = g[["Valor"]].resample("5min").mean().interpolate(method="time")
            g_resampled["Sensor_Id"] = sensor_id
            resampled_list.append(g_resampled)

        df_resampled = pd.concat(resampled_list).reset_index()

        # Redondeo de valores
        df_resampled["Valor"] = df_resampled["Valor"].round(2)

        # Crear features adicionales
        df_resampled["Hora"] = df_resampled["Fecha"].dt.hour
        df_resampled["DiaSemana"] = df_resampled["Fecha"].dt.day_name()

        # 3) CARGA
        df_resampled.to_csv(ruta_csv, index=False, encoding="utf-8")
        print(f"CSV ETL exportado a {ruta_csv} con {len(df_resampled)} registros.")

    except Exception as e:
        print(f"Error en ETL de exportación: {e}")
        raise RuntimeError(f"Error en ETL de exportación: {e}")



def etl_bitacoras(db: Session):
    try:
        # Extracción
        recolecciones = db.query(BitacoraRecoleccion).all()
        contenedores = db.query(BitacoraContenedor).all()

        # Transformación y limpieza
        data_recoleccion = []
        for r in recolecciones:
            if r.Fecha_Registro is None or r.Ruta_Id is None:
                continue  # Excluir nulos importantes

            duracion = r.Tiempo_Duracion if r.Tiempo_Duracion and r.Tiempo_Duracion <= 500 else None
            data_recoleccion.append({
                "ID": r.ID,
                "Fecha_Registro": r.Fecha_Registro.strftime("%Y-%m-%d %H:%M:%S"),
                "Ruta_Id": r.Ruta_Id,
                "Observaciones": r.Observaciones or "Sin observaciones",
                "Tiempo_Duracion": duracion,
                "Cantidad_Contenedores": r.Cantidad_Contenedores or 0
            })

        data_contenedor = []
        for c in contenedores:
            if c.Fecha_Registro is None or c.Contenedor_Id is None:
                continue

            porcentaje = c.Porcentaje_Llenado
            if porcentaje is not None and (porcentaje < 0 or porcentaje > 100):
                continue  # Valor atípico

            data_contenedor.append({
                "Bitacora_Id": c.Bitacora_Id,
                "Contenedor_Id": c.Contenedor_Id,
                "Fecha_Registro": c.Fecha_Registro.strftime("%Y-%m-%d %H:%M:%S"),
                "Estado_Contenedor": c.Estado_Contenedor or "Desconocido",
                "Porcentaje_Llenado": porcentaje,
                "Recolectado": c.Recolectado
            })

        # Carga: retornar DataFrames o guardarlos como CSV para análisis
        df_recoleccion = pd.DataFrame(data_recoleccion)
        df_contenedor = pd.DataFrame(data_contenedor)

        print(" ETL de bitácoras completado.")
        return df_recoleccion, df_contenedor

    except Exception as e:
        print(f" Error en ETL: {e}")
        return None, None