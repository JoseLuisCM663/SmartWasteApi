"""
Generador de lecturas para sensores.

Uso:
    from crud.seeder import generar_lecturas_sensor
    generar_lecturas_sensor(sensor_id=1, cantidad=100, valor_min=10, valor_max=90)
"""

from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from app.models.lectura_sensor import LecturaSensor
from app.database import SessionLocal
import random
from app.models.bitacora_recolecion import BitacoraRecoleccion
from app.models.bitacora_contenedor import BitacoraContenedor
from app.models.ruta_recoleccion import RutaRecoleccion
from app.models.contenedor import Contenedores

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
        print(f" {cantidad} lecturas generadas para el sensor {sensor_id}.")
    except Exception as e:
        db.rollback()
        print(f" Error al generar lecturas: {e}")
    finally:
        db.close()

def poblar_bitacoras(db: Session, cantidad: int = 5):
    """
    Crea registros ficticios en tbd_bitacora_recoleccion y tbd_bitacora_contenedor
    usando los IDs existentes de rutas y contenedores en la base de datos.

    :param db: Sesión activa de SQLAlchemy
    :param cantidad: Número de bitácoras a generar
    """

    # Obtener todos los IDs de rutas y contenedores existentes en la base de datos
    rutas_ids = [ruta.ID for ruta in db.query(RutaRecoleccion.ID).all()]
    contenedores_ids = [contenedor.ID for contenedor in db.query(Contenedores.ID).all()]

    if not rutas_ids or not contenedores_ids:
        print("No hay rutas o contenedores disponibles en la base de datos.")
        return

    for i in range(cantidad):
        ruta_id = random.choice(rutas_ids)
        fecha_evento = datetime.now() - timedelta(days=i)

        bitacora = BitacoraRecoleccion(
            Fecha_Registro=fecha_evento,
            Ruta_Id=ruta_id,
            Observaciones=random.choice([
                "Todo en orden.",
                "Derrame en contenedor.",
                "Obstrucción en vía.",
                "Demora por tráfico.",
                "Recolección parcial."
            ]),
            Tiempo_Duracion=random.randint(45, 120),
            Cantidad_Contenedores=random.randint(1, len(contenedores_ids))
        )
        db.add(bitacora)
        db.commit()
        db.refresh(bitacora)

        # Generar registros asociados a contenedores
        for cont_id in random.sample(contenedores_ids, k=bitacora.Cantidad_Contenedores):
            bitacora_contenedor = BitacoraContenedor(
                Bitacora_Id=bitacora.ID,
                Contenedor_Id=cont_id,
                Fecha_Registro=fecha_evento,
                Estado_Contenedor=random.choice(["Lleno", "Vaciado", "Dañado", "Obstruido"]),
                Porcentaje_Llenado=random.randint(20, 100),
                Recolectado=random.choice([True, False])
            )
            db.add(bitacora_contenedor)

    db.commit()
    print(f"Se generaron {cantidad} bitácoras con sus contenedores.")