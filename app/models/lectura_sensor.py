from sqlalchemy import Column, Integer, Float, DateTime, ForeignKey
from app.database import Base, is_sqlite

class LecturaSensor(Base):
    __tablename__ = 'tbd_lecturas_sensores'

    ID = Column(Integer, primary_key=True, autoincrement=not is_sqlite)
    Valor = Column(Float)
    Fecha = Column(DateTime)
    Sensor_Id = Column(Integer, ForeignKey("tbb_sensores.ID"), nullable=False)
