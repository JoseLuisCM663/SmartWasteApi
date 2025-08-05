from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.sensor import Sensor
from app.crud.seder import generar_lecturas_sensor
from datetime import datetime, timedelta
import random

router_seeder = APIRouter(
    prefix="/seeder",
    tags=["Seeder"]
)

@router_seeder.post("/generar-lecturas/")
def endpoint_generar_lecturas(
    sensor_id: int,
    cantidad: int = 10,
    valor_min: float = 10.0,
    valor_max: float = 100.0,
    intervalo_minutos: int = 5
):
    """
    Genera lecturas simuladas para un sensor.

    Parámetros:
    - sensor_id: ID del sensor.
    - cantidad: Número de lecturas a generar.
    - valor_min: Valor mínimo de lectura.
    - valor_max: Valor máximo de lectura.
    - intervalo_minutos: Espaciado de tiempo entre lecturas.
    """
    try:
        generar_lecturas_sensor(sensor_id, cantidad, valor_min, valor_max, intervalo_minutos)
        return {"mensaje": f"{cantidad} lecturas generadas para el sensor {sensor_id}"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
