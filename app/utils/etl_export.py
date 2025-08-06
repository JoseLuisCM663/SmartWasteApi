import pandas as pd
from sqlalchemy.orm import Session
from app.models.lectura_sensor import LecturaSensor
import numpy as np
from app.models.bitacora_recolecion import BitacoraRecoleccion
from app.models.bitacora_contenedor import BitacoraContenedor


def exportar_lecturas_sensor(sensor_id: int, ruta_csv: str, db: Session):
    """
    ETL completo de lecturas:
    - Extrae de la BD
    - Transforma: limpia, interpola, resamplea, crea features
    - Carga a CSV
    """
    try:
        # 1) EXTRACCIÓN
        lecturas = db.query(LecturaSensor) \
                     .filter(LecturaSensor.Sensor_Id == sensor_id) \
                     .all()

        # Convertir a lista de dicts
        data = [{
            "ID": l.ID,
            "Valor": l.Valor,
            "Fecha": l.Fecha,
        } for l in lecturas]

        df = pd.DataFrame(data)

        # 2) TRANSFORMACIÓN

        # a) Conversión Fecha a datetime y orden
        df["Fecha"] = pd.to_datetime(df["Fecha"])
        df = df.sort_values("Fecha")

        # b) Eliminación de duplicados
        df = df.drop_duplicates(subset=["Fecha"], keep="first")

        # c) Filtrado de valores válidos y clip
        df = df[df["Valor"].notna()]
        df["Valor"] = df["Valor"].clip(lower=0, upper=100)

        # d) Resampleo e interpolación
        #   • Índice temporal
        df = df.set_index("Fecha")
        #   • Resamplear a cada 5 minutos (o el intervalo que uses)
        df = df.resample("5T").mean()
        #   • Imputar valores faltantes por interpolación lineal
        df["Valor"] = df["Valor"].interpolate(method="time")

        # e) Redondeo
        df["Valor"] = df["Valor"].round(2)

        # f) Crear features adicionales
        df["Hora"] = df.index.hour
        df["DiaSemana"] = df.index.day_name()

        # 3) CARGA
        # Restaurar índice como columna
        df = df.reset_index()
        df.to_csv(ruta_csv, index=False)
        print(f"CSV ETL exportado a {ruta_csv}")

    except Exception as e:
        print(f"Error en ETL de exportación: {e}")


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