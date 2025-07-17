from sqlalchemy.orm import Session 
from app.models.usuario_ruta import UsuarioRuta
from app.schemas.usuario_ruta import UsuarioRutaCreate, UsuarioRutaUpdate, UsuarioRutaResponse
from datetime import datetime
from sqlalchemy import func
from fastapi import HTTPException, status

def create_usuario_ruta(db: Session, usuario_ruta: UsuarioRutaCreate) -> UsuarioRutaResponse:
    # Verifica si ya existe el registro con la misma clave primaria compuesta
    existente = db.query(UsuarioRuta).filter_by(
        Usuario_Id=usuario_ruta.Usuario_Id,
        Ruta_Id=usuario_ruta.Ruta_Id
    ).first()

    if existente:
        raise HTTPException(
            status_code=400,
            detail="El usuario ya está asignado a esta ruta."
        )

    db_usuario_ruta = UsuarioRuta(
        Usuario_Id=usuario_ruta.Usuario_Id,
        Ruta_Id=usuario_ruta.Ruta_Id,
        Fecha_Registro=datetime.utcnow(),
        Fecha_Actualizacion=None,
        Estatus=usuario_ruta.Estatus
    )

    db.add(db_usuario_ruta)
    db.commit()
    db.refresh(db_usuario_ruta)

    return UsuarioRutaResponse.from_orm(db_usuario_ruta)


def update_usuario_ruta(db: Session, usuario_ruta_id: int, usuario_ruta: UsuarioRutaUpdate) -> UsuarioRutaResponse:
    db_usuario_ruta = db.query(UsuarioRuta).filter(UsuarioRuta.ID == usuario_ruta_id).first()
    if not db_usuario_ruta:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuario Ruta not found")
    
    for key, value in usuario_ruta.dict(exclude_unset=True).items():
        setattr(db_usuario_ruta, key, value)
    
    db_usuario_ruta.Fecha_Actualizacion = datetime.utcnow()
    db.commit()
    db.refresh(db_usuario_ruta)
    return UsuarioRutaResponse.from_orm(db_usuario_ruta)

def get_usuario_ruta(db: Session, usuario_ruta_id: int) -> UsuarioRutaResponse:
    db_usuario_ruta = db.query(UsuarioRuta).filter(UsuarioRuta.ID== usuario_ruta_id).first()
    if not db_usuario_ruta:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuario Ruta not found")
    return UsuarioRutaResponse.from_orm(db_usuario_ruta)

def delete_usuario_ruta(db: Session, usuario_ruta_id: int) -> UsuarioRutaResponse:
    db_usuario_ruta = db.query(UsuarioRuta).filter(UsuarioRuta.ID == usuario_ruta_id).first()
    if not db_usuario_ruta:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuario Ruta not found")
    
    db.delete(db_usuario_ruta)
    db.commit()
    return UsuarioRutaResponse.from_orm(db_usuario_ruta)

def get_all_usuario_rutas(db: Session) -> list[UsuarioRutaResponse]:
    db_usuario_rutas = db.query(UsuarioRuta).all()
    return [UsuarioRutaResponse.from_orm(usuario_ruta) for usuario_ruta in db_usuario_rutas]

