from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base


class Sensor(Base):
    __tablename__ = 'tbb_sensores'
    ID = Column(Integer, primary_key=True, autoincrement=True, index=True)
    Tipo = Column(String(50), nullable=False)  # Tipo de sensor (ej. Ultrasonido, Infrarrojo, etc.)
    Descripcion = Column(String(255), nullable=True)
    Estatus = Column(Boolean, default=True)
    Fecha_Registro = Column(DateTime, nullable=False)
    Fecha_Actualizacion = Column(DateTime, nullable=True)
    Contenedor_Id = Column(Integer, ForeignKey("tbb_contenedores.ID"), nullable=False)
    Contenedor = relationship("Contenedor", back_populates="sensor")
    Lecturas = relationship("LecturaSensor", back_populates="sensor")
