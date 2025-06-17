from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.models.ruta_recoleccion import RutaRecoleccion
from app.schemas.ruta_recoleccion import RutaCreate, RutaOut, RutaUpdate
from app.crud.ruta_recolecion import (
    crear_ruta,
    obtener_ruta,
    actualizar_ruta,
    eliminar_ruta,
    listar_rutas
)
from app.database import get_db  # Asegúrate de importar get_db
from app.config.jwt import obtener_usuario_actual  # Importa desde config/jwt.py

router_ruta = APIRouter(
    prefix="/ruta_recoleccion",
    tags=["Rutas de Recolección"],
    dependencies=[Depends(obtener_usuario_actual)]  # Asegúrate de que el usuario esté autenticado
)

# Ruta para listar todas las rutas de recolección
@router_ruta.get("/", response_model=list[RutaOut])
def obtener_rutas(
    db: Session = Depends(get_db)
):
    """
    Endpoint para obtener todas las rutas de recolección.
    Requiere autenticación.
    """
    return listar_rutas(db)

# Ruta para crear una nueva ruta de recolección
@router_ruta.post("/", response_model=RutaOut)
def crear_nueva_ruta(
    ruta: RutaCreate,
    db: Session = Depends(get_db)
):
    """
    Endpoint para crear una nueva ruta de recolección.
    Requiere autenticación.
    """
    return crear_ruta(db, ruta)

# Ruta para obtener una ruta de recolección por ID
@router_ruta.get("/{ruta_id}", response_model=RutaOut)
def obtener_ruta_por_id(
    ruta_id: int,
    db: Session = Depends(get_db)
):
    """
    Endpoint para obtener una ruta de recolección por su ID.
    Requiere autenticación.
    """
    return obtener_ruta(db, ruta_id)

# Ruta para actualizar una ruta de recolección
@router_ruta.put("/{ruta_id}", response_model=RutaOut)
def actualizar_ruta_id(
    ruta_id: int,
    ruta: RutaUpdate,
    db: Session = Depends(get_db)
):
    """
    Endpoint para actualizar una ruta de recolección.
    Requiere autenticación.
    """
    return actualizar_ruta(db, ruta_id, ruta)

# Ruta para eliminar una ruta de recolección
@router_ruta.delete("/{ruta_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_ruta_id(
    ruta_id: int,
    db: Session = Depends(get_db)
):
    """
    Endpoint para eliminar una ruta de recolección.
    Requiere autenticación.
    """
    return eliminar_ruta(db, ruta_id)
