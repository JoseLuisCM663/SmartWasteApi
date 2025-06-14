from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy.orm import relationship
from app.database import Base

class RutaRecoleccion(Base):
    __tablename__ = 'tbb_rutas_recoleccion'
    ID = Column(Integer, primary_key=True,autoincrement=True, index=True)
    Nombre = Column(String(100), nullable=False)
    Descripcion = Column(String(255), nullable=True)
    Fecha_Registro = Column(DateTime, nullable=False)
    Fecha_Actualizacion = Column(DateTime, nullable=True)
    Estatus = Column(Boolean, default=True)
    Usuarios = relationship("User", secondary="usuario_ruta", back_populates="rutas")
    Contenedores = relationship("Contenedor", back_populates="ruta")
    Historiales = relationship("HistorialRecoleccion", back_populates="ruta")
