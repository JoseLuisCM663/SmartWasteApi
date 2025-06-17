from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.models.sensor import Sensor
from app.schemas.sensor import SensorCreate, SensorOut, SensorUpdate
from app.crud.sensor import (
    crear_sensor,
    obtener_sensor,
    actualizar_sensor,
    eliminar_sensor_por_id,
    listar_sensores,
    obtener_sensor_por_tipo
)
from app.database import get_db  # Asegúrate de importar get_db
from app.config.jwt import obtener_usuario_actual  # Importa desde config/jwt.py

router_sensor = APIRouter(
    prefix="/sensor",
    tags=["Sensores"],
    dependencies=[Depends(obtener_usuario_actual)]  # Asegúrate de que el usuario esté autenticado
)

# Ruta para listar todos los sensores
@router_sensor.get("/", response_model=list[SensorOut])
def listar_todos_los_sensores(
    db: Session = Depends(get_db)
):
    """
    Endpoint para obtener todos los sensores.
    Requiere autenticación.
    """
    return listar_sensores(db)

# Ruta para crear un nuevo sensor
@router_sensor.post("/", response_model=SensorOut)
def crear_nuevo_sensor(
    sensor: SensorCreate,
    db: Session = Depends(get_db)
):
    """
    Endpoint para crear un nuevo sensor.
    Requiere autenticación.
    """
    return crear_sensor(db, sensor)

# Ruta para obtener un sensor por ID
@router_sensor.get("/{sensor_id}", response_model=SensorOut)
def obtener_sensor_por_id(
    sensor_id: int,
    db: Session = Depends(get_db)
):
    """
    Endpoint para obtener un sensor por su ID.
    Requiere autenticación.
    """
    return obtener_sensor(db, sensor_id)

# Ruta para actualizar un sensor
@router_sensor.put("/{sensor_id}", response_model=SensorOut)
def actualizar_sensor_por_id(
    sensor_id: int,
    sensor: SensorUpdate,
    db: Session = Depends(get_db)
):
    """
    Endpoint para actualizar un sensor.
    Requiere autenticación.
    """
    return actualizar_sensor(db, sensor_id, sensor)

# Ruta para eliminar un sensor por ID
@router_sensor.delete("/{sensor_id}", response_model=dict)
def eliminar_sensor(
    sensor_id: int,
    db: Session = Depends(get_db)
):
    """
    Endpoint para eliminar un sensor por su ID.
    Requiere autenticación.
    """
    return eliminar_sensor_por_id(db, sensor_id)

# Ruta para obtener un sensor por tipo
@router_sensor.get("/tipo/{tipo}", response_model=SensorOut)
def obtener_sensor_por_tipo_endpoint(
    tipo: str,
    db: Session = Depends(get_db)
):
    """
    Endpoint para obtener un sensor por su tipo.
    Requiere autenticación.
    """
    sensor = obtener_sensor_por_tipo(db, tipo)
    if not sensor:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Sensor no encontrado")
    return sensor

