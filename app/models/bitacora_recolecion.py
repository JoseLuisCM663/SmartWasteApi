from sqlalchemy import Column, Integer, DateTime, ForeignKey, String
from app.database import Base, is_sqlite

class BitacoraRecoleccion(Base):
    __tablename__ = 'tbd_bitacora_recoleccion'

    ID = Column(Integer, primary_key=True, autoincrement=not is_sqlite)
    Fecha_Registro = Column(DateTime, nullable=False)
    Ruta_Id = Column(Integer, ForeignKey("tbb_rutas_recoleccion.ID"))
    Observaciones = Column(String(255), nullable=True)
    Tiempo_Duracion = Column(Integer, nullable=True)
    Cantidad_Contenedores = Column(Integer, nullable=True)
