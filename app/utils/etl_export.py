import pandas as pd
from sqlalchemy.orm import Session
from app.models.lectura_sensor import LecturaSensor


def exportar_lecturas_sensor(sensor_id: int, ruta_csv: str, db: Session):
    try:
        lecturas = db.query(LecturaSensor).filter(LecturaSensor.Sensor_Id == sensor_id).all()

        data = [
            {
                "ID": l.ID,
                "Valor": l.Valor,
                "Fecha": l.Fecha.strftime("%Y-%m-%d %H:%M:%S"),
                "Sensor_Id": l.Sensor_Id
            }
            for l in lecturas
            if l.Valor is not None and 0 <= l.Valor <= 100
        ]

        df = pd.DataFrame(data)
        df.to_csv(ruta_csv, index=False)
        print(f"✅ CSV exportado a {ruta_csv}")

    except Exception as e:
        print(f"❌ Error al exportar: {e}")

