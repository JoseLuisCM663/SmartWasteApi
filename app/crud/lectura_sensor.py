from sqlalchemy.orm import Session 
from app.models.lectura_sensor import LecturaSensor
from app.schemas.lectura_sensor import LecturaSensorCreate, LecturaSensorRead
from datetime import datetime
from sqlalchemy import func
from fastapi import HTTPException, status

# Funcion para crear una nueva lectura de sensor
def crear_lectura_sensor(db: Session, lectura: LecturaSensorCreate):
    nueva_lectura = LecturaSensor(
        Valor=lectura.Valor,
        Fecha=datetime.now(),  # Asignar la fecha actual
        Sensor_Id=lectura.Sensor_Id,

    )
    db.add(nueva_lectura)
    db.commit()
    db.refresh(nueva_lectura)
    return nueva_lectura

# Funcion para obtener una lectura por Fecha
def obtener_lectura_por_fecha(db: Session, fecha: datetime):
    lectura = db.query(LecturaSensor).filter(LecturaSensor.Fecha == fecha).first()
    if not lectura:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Lectura no encontrada")
    return lectura

# Funcion para obtener una lectura por sensor
def obtener_lectura_por_sensor(db: Session, sensor_id: int):
    lecturas = db.query(LecturaSensor).filter(LecturaSensor.Sensor_Id == sensor_id).all()
    if not lecturas:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No se encontraron lecturas para este sensor")
    return lecturas

#Funcion por Promedios
def obtener_promedio_lecturas_por_sensor(db: Session, sensor_id: int):
    promedio = db.query(func.avg(LecturaSensor.Valor)).filter(LecturaSensor.Sensor_Id == sensor_id).scalar()
    if promedio is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No se encontraron lecturas para este sensor")
    return promedio

# Funcion para obtener todas las lecturas de un sensor
def obtener_todas_las_lecturas_por_sensor(db: Session, sensor_id: int):
    lecturas = db.query(LecturaSensor).filter(LecturaSensor.Sensor_Id == sensor_id).all()
    if not lecturas:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No se encontraron lecturas para este sensor")
    return lecturas

# Funcion para obtener máximos y mínimos de lecturas por sensor
def obtener_maximo_minimo_lecturas_por_sensor(db: Session, sensor_id: int):
    maximo = db.query(func.max(LecturaSensor.Valor)).filter(LecturaSensor.Sensor_Id == sensor_id).scalar()
    minimo = db.query(func.min(LecturaSensor.Valor)).filter(LecturaSensor.Sensor_Id == sensor_id).scalar()
    
    if maximo is None or minimo is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No se encontraron lecturas para este sensor")
    
    return {"maximo": maximo, "minimo": minimo}