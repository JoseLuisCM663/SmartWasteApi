from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey
from app.database import Base, is_sqlite

class Sensor(Base):
    __tablename__ = 'tbb_sensores'

    ID = Column(Integer, primary_key=True, autoincrement=not is_sqlite, index=True)
    Tipo = Column(String(50), nullable=False)
    Descripcion = Column(String(255), nullable=True)
    Estatus = Column(Boolean, default=True)
    Fecha_Registro = Column(DateTime, nullable=False)
    Fecha_Actualizacion = Column(DateTime, nullable=True)
    Contenedor_Id = Column(Integer, ForeignKey("tbb_contenedores.ID"), nullable=True)
