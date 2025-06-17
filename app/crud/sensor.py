from sqlalchemy.orm import Session
from app.models.sensor import Sensor        
from app.schemas.sensor import SensorCreate, SensorOut, SensorUpdate
from datetime import datetime
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status

#function to create a new sensor
def crear_sensor(db: Session, sensor: SensorCreate):
    nuevo_sensor = Sensor(
        Descripcion=sensor.Descripcion,
        Tipo=sensor.Tipo,
        Estatus=sensor.Estatus,
        Fecha_Registro=datetime.now(),
        Fecha_Actualizacion=datetime.now(),
        Contenedor_Id=sensor.Contenedor_Id if sensor.Contenedor_Id else None
    )
    db.add(nuevo_sensor)
    db.commit()
    db.refresh(nuevo_sensor)
    return nuevo_sensor

# function to get a sensor by ID
def obtener_sensor(db: Session, sensor_id: int):
    sensor = db.query(Sensor).filter(Sensor.ID == sensor_id).first()
    if not sensor:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Sensor no encontrado")
    return sensor

# function to update a sensor
def actualizar_sensor(db: Session, sensor_id: int, sensor_update: SensorUpdate):
    sensor = db.query(Sensor).filter(Sensor.ID == sensor_id).first()
    if not sensor:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Sensor no encontrado")
    
    for key, value in sensor_update.dict(exclude_unset=True).items():
        setattr(sensor, key, value)
    
    sensor.Fecha_Actualizacion = datetime.now()
    db.commit()
    db.refresh(sensor)
    return sensor

#funcion eliminar sensor por id
def eliminar_sensor_por_id(db: Session, sensor_id: int):
    sensor = db.query(Sensor).filter(Sensor.ID == sensor_id).first()
    if not sensor:
        raise HTTPException(status_code=404, detail="Sensor no encontrado")
    try:
        db.delete(sensor)
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail="No se puede eliminar el sensor porque tiene lecturas asociadas"
        )
    return {"message": "Sensor eliminado correctamente"}

# function to list all sensors
def listar_sensores(db: Session):
    sensores = db.query(Sensor).all()
    return sensores

# function to get a sensor by type
def obtener_sensor_por_tipo(db: Session, tipo: str):
    sensor = db.query(Sensor).filter(Sensor.Tipo == tipo).first()
    if not sensor:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Sensor no encontrado")
    return sensor
