from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class RutaBase(BaseModel):
    Nombre: str
    Descripcion: Optional[str] = None
    Estatus: Optional[bool] = True

class RutaCreate(RutaBase):
    pass

class RutaUpdate(BaseModel):
    Nombre: Optional[str]
    Descripcion: Optional[str]
    Estatus: Optional[bool]
    Fecha_Actualizacion: Optional[datetime]

class RutaOut(RutaBase):
    ID: int
    Fecha_Registro: datetime
    Fecha_Actualizacion: Optional[datetime]

    class Config:
        orm_mode = True
