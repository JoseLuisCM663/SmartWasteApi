from sqlalchemy import Column, Integer, DateTime, ForeignKey, String, Boolean
from sqlalchemy.orm import relationship 
from app.database import Base

class BitacoraRecoleccion(Base):
    __tablename__ = 'tbd_bitacora_recoleccion'
    ID = Column(Integer, primary_key=True)
    Fecha_Registro = Column(DateTime, nullable=False)  # Fecha exacta del evento de recolección
    Ruta_Id = Column(Integer, ForeignKey("tbb_rutas_recoleccion.ID"))

    Observaciones = Column(String(255), nullable=True)  # Texto libre, por si hubo problemas
    Tiempo_Duracion = Column(Integer, nullable=True)  # Duración estimada/en minutos
    Cantidad_Contenedores = Column(Integer, nullable=True)  # Cuántos contenedores se atendieron
    