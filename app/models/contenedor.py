from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, DateTime
from app.database import Base, is_sqlite

class Contenedores(Base):
    __tablename__ = 'tbb_contenedores'

    ID = Column(Integer, primary_key=True, autoincrement=not is_sqlite, index=True)
    Ubicacion = Column(String(255), nullable=False)
    Capacidad = Column(Integer, nullable=False)
    Ruta_Id = Column(Integer, ForeignKey("tbb_rutas_recoleccion.ID"), nullable=True)
    Descripcion = Column(String(255), nullable=True)
    Estatus = Column(Boolean, default=True)
    Fecha_Registro = Column(DateTime)
    Fecha_Actualizacion = Column(DateTime, nullable=True)
