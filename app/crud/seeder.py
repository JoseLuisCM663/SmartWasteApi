from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from app.models.lectura_sensor import LecturaSensor
from app.database import SessionLocal
import random

def generar_lecturas_sensor(sensor_id: int, cantidad: int, valor_min: float, valor_max: float, intervalo_minutos: int = 5):
    """
    Genera lecturas aleatorias para un sensor específico.

    :param sensor_id: ID del sensor al que se le asignarán las lecturas
    :param cantidad: Número de lecturas a generar
    :param valor_min: Valor mínimo posible de lectura
    :param valor_max: Valor máximo posible de lectura
    :param intervalo_minutos: Intervalo en minutos entre lecturas simuladas
    """
    db: Session = SessionLocal()

    try:
        ahora = datetime.now()

        for i in range(cantidad):
            lectura = LecturaSensor(
                Valor=round(random.uniform(valor_min, valor_max), 2),
                Fecha=ahora - timedelta(minutes=i * intervalo_minutos),
                Sensor_Id=sensor_id
            )
            db.add(lectura)

        db.commit()
        print(f"✅ {cantidad} lecturas generadas para el sensor {sensor_id}.")
    except Exception as e:
        db.rollback()
        print(f"❌ Error al generar lecturas: {e}")
    finally:
        db.close()
