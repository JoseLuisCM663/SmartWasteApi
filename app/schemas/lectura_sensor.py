from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class LecturaSensorBase(BaseModel):
    Valor: float
    Fecha: datetime
    Sensor_Id: Optional[int] = None

class LecturaSensorCreate(LecturaSensorBase):
    pass

class LecturaSensorRead(LecturaSensorBase):
    ID: int

    class Config:
        from_attributes = True  # reemplazo moderno de orm_mode

