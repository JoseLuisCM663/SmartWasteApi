from sqlalchemy.orm import Session 
from app.models.contenedor import Contenedores
from app.schemas.contenedor import ContenedorCreate, ContenedorUpdate, ContenedorBase
from datetime import datetime
from fastapi import HTTPException, status

# Funcion para crear un nuevo contenedor
def crear_contenedor(db: Session, contenedor: ContenedorCreate):
    nuevo_contenedor = Contenedores(
        Ubicacion=contenedor.Ubicacion,
        Capacidad=contenedor.Capacidad,
        Ruta_Id=contenedor.Ruta_Id if contenedor.Ruta_Id is not None else None,
        Descripcion=contenedor.Descripcion,
        Estatus=contenedor.Estatus,
        Fecha_Registro=datetime.now(),
        Fecha_Actualizacion=datetime.now()
        
    )
    db.add(nuevo_contenedor)
    db.commit()
    db.refresh(nuevo_contenedor)
    return nuevo_contenedor

# Funcion para obtener un contenedor por ID
def obtener_contenedor(db: Session, contenedor_id: int):
    contenedor = db.query(Contenedores).filter(Contenedores.ID == contenedor_id).first()
    if not contenedor:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contenedor no encontrado")
    return contenedor

# Funcion para actualizar un contenedor
def actualizar_contenedor(db: Session, contenedor_id: int, contenedor_update: ContenedorUpdate):
    contenedor = db.query(Contenedores).filter(Contenedores.ID == contenedor_id).first()
    if not contenedor:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contenedor no encontrado")
    
    for key, value in contenedor_update.dict(exclude_unset=True).items():
        setattr(contenedor, key, value)
    
    contenedor.Fecha_Actualizacion = datetime.now()
    db.commit()
    db.refresh(contenedor)
    return contenedor

# Funcion para eliminar un contenedor
def eliminar_contenedor_id(db: Session, contenedor_id: int):
    contenedor = db.query(Contenedores).filter(Contenedores.ID == contenedor_id).first()
    if not contenedor:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contenedor no encontrado")
    
    db.delete(contenedor)
    db.commit()
    return {"detail": "Contenedor eliminado exitosamente"}

# Funcion para listar todos los contenedores
def listar_contenedores(db: Session):
    contenedores = db.query(Contenedores).all()
    return contenedores

# Funcion para filtrar contenedores por ruta
def filtrar_contenedores_por_ruta(db: Session, ruta_id: int):
    contenedores = db.query(Contenedores).filter(Contenedores.Ruta_Id == ruta_id).all()
    if not contenedores:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No se encontraron contenedores para esta ruta")
    return contenedores

# Funcion para filtrar contenedores por ubicacion
def filtrar_contenedores_por_ubicacion(db: Session, ubicacion: str):
    contenedores = db.query(Contenedores).filter(Contenedores.Ubicacion == ubicacion).all()
    if not contenedores:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No se encontraron contenedores en esta ubicacion")
    return contenedores

# Funcion para filtrar contenedores por estatus
def filtrar_contenedores_por_estatus(db: Session, estatus: bool):
    contenedores = db.query(Contenedores).filter(Contenedores.Estatus == estatus).all()
    if not contenedores:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No se encontraron contenedores con este estatus")
    return contenedores

