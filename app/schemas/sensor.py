from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class SensorBase(BaseModel):
    Tipo: str
    Descripcion: Optional[str] = None
    Estatus: Optional[bool] = True
    Contenedor_Id: Optional[int] = None

class SensorCreate(SensorBase):
    pass

class SensorUpdate(BaseModel):
    Tipo: Optional[str]
    Descripcion: Optional[str]
    Estatus: Optional[bool]
    Contenedor_Id: Optional[int] = None
    Fecha_Actualizacion: Optional[datetime]

class SensorOut(SensorBase):
    ID: int
    Fecha_Registro: datetime
    Fecha_Actualizacion: Optional[datetime]

    class Config:
        orm_mode = True
