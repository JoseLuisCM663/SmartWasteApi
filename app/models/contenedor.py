from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, DateTime as DataTime
from sqlalchemy.orm import relationship
from app.database import Base


class Contenedor(Base):
    __tablename__ = 'tbb_contenedores'
    ID = Column(Integer, primary_key=True, autoincrement=True, index=True)
    Ubicacion = Column(String(255), nullable=False)  # Ubicación del contenedor
    Capacidad = Column(Integer, nullable=False)  # Capacidad del contenedor en litros
    Ruta_Id = Column(Integer, ForeignKey("tbb_rutas_recoleccion.ID"))
    Descripcion = Column(String(255), nullable=True)
    Estatus = Column(Boolean, default=True)
    Fecha_Registro = Column(DataTime)  # Cambiado a String para simplificar, puedes usar DateTime si prefieres
    Fecha_Actualizacion = Column(DataTime, nullable=True)
    Ruta = relationship("RutaRecoleccion", back_populates="contenedores")
    Sensor = relationship("Sensor", uselist=False, back_populates="contenedor")
    Historiales = relationship("HistorialContenedor", back_populates="contenedor")
