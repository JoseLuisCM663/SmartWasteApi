from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship 
from app.database import Base

class BitacoraContenedor(Base):
    __tablename__ = 'tbd_bitacora_contenedor'
    Bitacora_Id = Column(Integer, ForeignKey("tbd_bitacora_recoleccion.ID"), primary_key=True)
    Contenedor_Id = Column(Integer, ForeignKey("tbb_contenedores.ID"), primary_key=True)




