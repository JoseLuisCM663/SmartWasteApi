from sqlalchemy.orm import Session 
from app.models.contenedor import Contenedor
from app.schemas.contenedor import ContenedorCreate, ContenedorUpdate, ContenedorBase
from datetime import datetime
from fastapi import HTTPException, status

# Funcion para crear un nuevo contenedor
def crear_contenedor(db: Session, contenedor: ContenedorCreate):
    nuevo_contenedor = Contenedor(
        Ubicacion=contenedor.Ubicacion,
    )