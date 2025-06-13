from sqlalchemy import Column, Integer, ForeignKey, DateTime, Boolean
from app.database import Base

class UsuarioRuta(Base):
    __tablename__ = 'tbc_usuario_ruta'
    Usuario_Id = Column(Integer, ForeignKey("tbb_usuarios.ID"), primary_key=True)
    Ruta_Id = Column(Integer, ForeignKey("tbb_rutas_recoleccion.ID"), primary_key=True)
    Fecha_Registro = Column(DateTime, nullable=False)
    Fecha_Actualizacion = Column(DateTime, nullable=True)
    Estatus = Column(Boolean, default=True)


