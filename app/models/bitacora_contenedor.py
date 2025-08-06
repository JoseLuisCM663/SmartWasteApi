from sqlalchemy import Column, Integer, ForeignKey, DateTime, String, Boolean
from sqlalchemy.orm import relationship 
from app.database import Base

class BitacoraContenedor(Base):
    __tablename__ = 'tbd_bitacora_contenedor'
    Bitacora_Id = Column(Integer, ForeignKey("tbd_bitacora_recoleccion.ID"), primary_key=True)
    Contenedor_Id = Column(Integer, ForeignKey("tbb_contenedores.ID"), primary_key=True)

    Fecha_Registro = Column(DateTime, nullable=False)  # Fecha exacta del evento de recolección
    Estado_Contenedor = Column(String(100), nullable=True)  # Ej: "Lleno", "Vaciado", "Dañado", "Obstruido"
    Porcentaje_Llenado = Column(Integer, nullable=True)  # Ej: 75 (%), si hay sensor de nivel
    Recolectado = Column(Boolean, default=False)  # Si se vació efectivamente



