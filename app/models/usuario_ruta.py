from sqlalchemy import Column, Integer, ForeignKey, DateTime, Boolean
from app.database import Base

class UsuarioRuta(Base):
    __tablename__ = 'tbc_usuario_ruta'
    Usuario_Id = Column(Integer, ForeignKey("tbb_usuarios.ID"), primary_key=True)
    Ruta_Id = Column(Integer, ForeignKey("tbb_rutas_recoleccion.ID"), primary_key=True)
    Fecha_Asignacion = Column(DateTime, nullable=False)
    Estatus = Column(Boolean, default=True)


