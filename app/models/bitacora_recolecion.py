from sqlalchemy import Column, Integer, DateTime, ForeignKey
from sqlalchemy.orm import relationship 
from app.database import Base

class BitacoraRecoleccion(Base):
    __tablename__ = 'tbd_bitacora_recoleccion'
    ID = Column(Integer, primary_key=True)
    Fecha = Column(DateTime)
    Ruta_Id = Column(Integer, ForeignKey("tbb_rutas_recoleccion.ID"))

