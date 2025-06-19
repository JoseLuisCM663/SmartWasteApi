from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.models.lectura_sensor import LecturaSensor
from app.schemas.lectura_sensor import LecturaSensorCreate, LecturaSensorRead
from app.crud.lectura_sensor import (
    crear_lectura_sensor,
    obtener_lectura_por_fecha,
    obtener_lectura_por_sensor,
    obtener_promedio_lecturas_por_sensor,
    obtener_todas_las_lecturas_por_sensor,
    obtener_maximo_minimo_lecturas_por_sensor
)
from datetime import datetime
from app.database import get_db  # Asegúrate de importar get_db
from datetime import timedelta


router_lectura_sensor = APIRouter(
    prefix="/lectura_sensor",
    tags=["Lectura Sensor"],
)

# Ruta para crear una nueva lectura de sensor
@router_lectura_sensor.post("/", response_model=LecturaSensorRead, status_code=status.HTTP_201_CREATED)
def crear_lectura(lectura: LecturaSensorCreate, db: Session = Depends(get_db)):
    """
    Crea una nueva lectura de sensor.
    """
    return crear_lectura_sensor(db=db, lectura=lectura)

# Ruta para obtener una lectura por fecha
@router_lectura_sensor.get("/{fecha}", response_model=LecturaSensorRead)
def obtener_lectura_fecha(fecha: datetime, db: Session = Depends(get_db)):
    """
    Obtiene una lectura de sensor por fecha.
    """
    return obtener_lectura_por_fecha(db=db, fecha=fecha)


# Ruta para obtener lecturas por sensor
@router_lectura_sensor.get("/sensor/{sensor_id}", response_model=list[LecturaSensorRead])
def obtener_lecturas_por_sensor(sensor_id: int, db: Session = Depends(get_db)):
    """
    Obtiene todas las lecturas de un sensor.
    """
    return obtener_lectura_por_sensor(db=db, sensor_id=sensor_id)

# Ruta para obtener el promedio de lecturas por sensor
@router_lectura_sensor.get("/sensor/{sensor_id}/promedio", response_model=float)
def obtener_promedio_lecturas_sensor(sensor_id: int, db: Session = Depends(get_db)):
    """
    Obtiene el promedio de las lecturas de un sensor.
    """
    return obtener_promedio_lecturas_por_sensor(db=db, sensor_id=sensor_id)

# Ruta para obtener todas las lecturas de un sensor
@router_lectura_sensor.get("/sensor/{sensor_id}/todas", response_model=list[LecturaSensorRead])
def obtener_todas_las_lecturas_sensor(sensor_id: int, db: Session = Depends(get_db)):
    """
    Obtiene todas las lecturas de un sensor.
    """
    return obtener_todas_las_lecturas_por_sensor(db=db, sensor_id=sensor_id)

# Ruta para obtener máximos y mínimos de lecturas por sensor
@router_lectura_sensor.get("/sensor/{sensor_id}/max-min", response_model=dict)
def obtener_maximo_minimo_lecturas_sensor(sensor_id: int, db: Session = Depends(get_db)):
    """
    Obtiene los valores máximos y mínimos de las lecturas de un sensor.
    """
    return obtener_maximo_minimo_lecturas_por_sensor(db=db, sensor_id=sensor_id)