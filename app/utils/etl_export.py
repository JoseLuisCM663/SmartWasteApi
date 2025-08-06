import pandas as pd
from sqlalchemy.orm import Session
from app.models.lectura_sensor import LecturaSensor
import numpy as np


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
