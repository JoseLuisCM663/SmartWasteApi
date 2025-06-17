from sqlalchemy import Column, Integer, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class LecturaSensor(Base):
    __tablename__ = 'tbd_lecturas_sensores'
    ID = Column(Integer, primary_key=True)
    Valor = Column(Float)
    Fecha = Column(DateTime)
    Sensor_Id = Column(Integer, ForeignKey("tbb_sensores.ID"), nullable=False)

