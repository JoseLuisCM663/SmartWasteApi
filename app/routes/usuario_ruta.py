from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.models.usuario_ruta import UsuarioRuta
from app.schemas.usuario_ruta import UsuarioRutaCreate, UsuarioRutaUpdate, UsuarioRutaResponse
from app.crud.usuario_ruta import (
    create_usuario_ruta,
    update_usuario_ruta,
    get_usuario_ruta,
    delete_usuario_ruta,
    get_all_usuario_rutas
)
from datetime import datetime
from app.database import get_db  # Asegúrate de importar get_db
from datetime import timedelta


router_usuario_ruta = APIRouter(
    prefix="/usuario_ruta",
   tags=["usuario_ruta"]
)
# Ruta para crear una nueva relación usuario-ruta
@router_usuario_ruta.post("/", response_model=UsuarioRutaResponse, status_code=status.HTTP_201_CREATED)
def crear_usuario_ruta(usuario_ruta: UsuarioRutaCreate, db: Session = Depends(get_db)):
    """
    Crea una nueva relación entre un usuario y una ruta.
    """
    return create_usuario_ruta(db=db, usuario_ruta=usuario_ruta)

# Ruta para actualizar una relación usuario-ruta
@router_usuario_ruta.put("/{usuario_ruta_id}", response_model=UsuarioRutaResponse)
def actualizar_usuario_ruta(usuario_ruta_id: int, usuario_ruta: UsuarioRutaUpdate, db: Session = Depends(get_db)):
    """
    Actualiza una relación existente entre un usuario y una ruta.
    """
    return update_usuario_ruta(db=db, usuario_ruta_id=usuario_ruta_id, usuario_ruta=usuario_ruta)   

# Ruta para obtener una relación usuario-ruta por ID
@router_usuario_ruta.get("/{usuario_ruta_id}", response_model=UsuarioRutaResponse)
def obtener_usuario_ruta(usuario_ruta_id: int, db: Session = Depends(get_db)):
    """
    Obtiene una relación existente entre un usuario y una ruta por su ID.
    """
    return get_usuario_ruta(db=db, usuario_ruta_id=usuario_ruta_id)

# Ruta para eliminar una relación usuario-ruta por ID
@router_usuario_ruta.delete("/{usuario_ruta_id}", response_model=UsuarioRutaResponse)
def eliminar_usuario_ruta(usuario_ruta_id: int, db: Session = Depends(get_db)):
    """
    Elimina una relación existente entre un usuario y una ruta por su ID.
    """
    return delete_usuario_ruta(db=db, usuario_ruta_id=usuario_ruta_id)

# Ruta para obtener todas las relaciones usuario-ruta
@router_usuario_ruta.get("/", response_model=list[UsuarioRutaResponse])
def obtener_todas_las_relaciones_usuario_ruta(db: Session = Depends(get_db)):
    """
    Obtiene todas las relaciones entre usuarios y rutas.
    """
    return get_all_usuario_rutas(db=db)

