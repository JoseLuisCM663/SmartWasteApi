from sqlalchemy.orm import Session 
from app.models.ruta_recoleccion import RutaRecoleccion
from app.schemas.ruta_recoleccion import RutaCreate,RutaOut, RutaUpdate
from datetime import datetime
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status

# Funcion para crear una nueva ruta de recoleccion
def crear_ruta(db: Session, ruta: RutaCreate):
    nueva_ruta = RutaRecoleccion(
        Nombre=ruta.Nombre,
        Descripcion=ruta.Descripcion,
        Estatus=ruta.Estatus,
        Fecha_Registro=datetime.now(),
        Fecha_Actualizacion=datetime.now()
    )
    db.add(nueva_ruta)
    db.commit()
    db.refresh(nueva_ruta)
    return nueva_ruta

# Funcion para obtener una ruta por ID
def obtener_ruta(db: Session, ruta_id: int):
    ruta = db.query(RutaRecoleccion).filter(RutaRecoleccion.ID == ruta_id).first()
    if not ruta:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Ruta no encontrada")
    return ruta

# Funcion para actualizar una ruta
def actualizar_ruta(db: Session, ruta_id: int, ruta_update: RutaUpdate):
    ruta = db.query(RutaRecoleccion).filter(RutaRecoleccion.ID == ruta_id).first()
    if not ruta:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Ruta no encontrada")
    
    for key, value in ruta_update.dict(exclude_unset=True).items():
        setattr(ruta, key, value)
    
    ruta.Fecha_Actualizacion = datetime.now()
    db.commit()
    db.refresh(ruta)
    return ruta

# Funcion para eliminar una ruta
def eliminar_ruta(db: Session, ruta_id: int):
    ruta = db.query(RutaRecoleccion).filter(RutaRecoleccion.ID == ruta_id).first()
    if not ruta:
        raise HTTPException(status_code=404, detail="Ruta no encontrada")
    try:
        db.delete(ruta)
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail="No se puede eliminar la ruta porque tiene contenedores asociados"
        )
    return {"message": "Ruta eliminada correctamente"}

# Funcion para listar todas las rutas
def listar_rutas(db: Session):
    rutas = db.query(RutaRecoleccion).all()
    return rutas

