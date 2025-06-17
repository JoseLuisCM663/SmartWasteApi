from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.models.contenedor import Contenedores
from app.models.usuarios import Usuario
from app.schemas.contenedor import ContenedorCreate, ContenedorResponse
from app.crud.contenedor import (
    crear_contenedor,
    actualizar_contenedor,
    eliminar_contenedor_id,
    obtener_contenedor,
    listar_contenedores,
    filtrar_contenedores_por_ruta,
    filtrar_contenedores_por_ubicacion,
    filtrar_contenedores_por_estatus
)
from app.database import get_db  # Asegúrate de importar get_db
from datetime import timedelta
from app.config.jwt import obtener_usuario_actual  # Importa desde config/jwt.py

router_contenedor = APIRouter(
    prefix="/contenedor",
    tags=["Contenedores"],
    dependencies=[Depends(obtener_usuario_actual)]  # << Esta línea soluciona el problema
)

# Ruta para listar todos los contenedores

@router_contenedor.get("/", response_model=list[ContenedorResponse])
def obtener_contenedores(
    db: Session = Depends(get_db)
    ):
    """
    Endpoint para obtener todos los contenedores.
    Requiere autenticación.
    """
    return listar_contenedores(db)

# Ruta para crear un nuevo contenedor
@router_contenedor.post("/", response_model=ContenedorResponse)
def crear_nuevo_contenedor(
    contenedor: ContenedorCreate,
    db: Session = Depends(get_db)
):
    """
    Endpoint para crear un nuevo contenedor.
    Requiere autenticación.
    """
    return crear_contenedor(db, contenedor)

# Ruta para obtener un contenedor por ID
@router_contenedor.get("/{contenedor_id}", response_model=ContenedorResponse)
def obtener_contenedor_por_id(
    contenedor_id: int,
    db: Session = Depends(get_db)
):
    """
    Endpoint para obtener un contenedor por su ID.
    Requiere autenticación.
    """
    return obtener_contenedor(db, contenedor_id)

# Ruta para actualizar un contenedor
@router_contenedor.put("/{contenedor_id}", response_model=ContenedorResponse)
def actualizar_contenedor_id(
    contenedor_id: int,
    contenedor: ContenedorCreate,
    db: Session = Depends(get_db)
):
    """
    Endpoint para actualizar un contenedor.
    Requiere autenticación.
    """
    return actualizar_contenedor(db, contenedor_id, contenedor)

# Ruta para eliminar un contenedor
@router_contenedor.delete("/{contenedor_id}", response_model=dict)    
def eliminar_contenedor(
    contenedor_id: int,
    db: Session = Depends(get_db)
):
    """
    Endpoint para eliminar un contenedor.
    Requiere autenticación.
    """
    return eliminar_contenedor_id(db, contenedor_id)

# Ruta para filtrar contenedores por ruta
@router_contenedor.get("/ruta/{ruta_id}", response_model=list[ContenedorResponse])
def filtrar_contenedores_ruta(
    ruta_id: int,
    db: Session = Depends(get_db)
):
    """
    Endpoint para filtrar contenedores por ruta.
    Requiere autenticación.
    """
    return filtrar_contenedores_por_ruta(db, ruta_id)

# Ruta para filtrar contenedores por ubicación
@router_contenedor.get("/ubicacion/{ubicacion}", response_model=list[ContenedorResponse])
def filtrar_contenedores_ubicacion(
    ubicacion: str,
    db: Session = Depends(get_db)
):
    """
    Endpoint para filtrar contenedores por ubicación.
    Requiere autenticación.
    """
    return filtrar_contenedores_por_ubicacion(db, ubicacion)

# Ruta para filtrar contenedores por estatus
@router_contenedor.get("/estatus/{estatus}", response_model=list[ContenedorResponse])
def filtrar_contenedores_estatus(
    estatus: str,
    db: Session = Depends(get_db)
):
    """
    Endpoint para filtrar contenedores por estatus.
    Requiere autenticación.
    """
    return filtrar_contenedores_por_estatus(db, estatus)

