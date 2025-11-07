from sqlalchemy import Column, Integer, ForeignKey, DateTime, String, Boolean
from app.database import Base, is_sqlite

class BitacoraContenedor(Base):
    __tablename__ = 'tbd_bitacora_contenedor'

    # Evita autoincrement en SQLite para llaves compuestas
    Bitacora_Id = Column(Integer, ForeignKey("tbd_bitacora_recoleccion.ID"), primary_key=True, autoincrement=not is_sqlite)
    Contenedor_Id = Column(Integer, ForeignKey("tbb_contenedores.ID"), primary_key=True)
    Fecha_Registro = Column(DateTime, nullable=False)
    Estado_Contenedor = Column(String(100), nullable=True)
    Porcentaje_Llenado = Column(Integer, nullable=True)
    Recolectado = Column(Boolean, default=False)
