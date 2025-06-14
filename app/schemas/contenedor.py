from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class ContenedorBase(BaseModel):
    Ubicacion: str
    Capacidad: int
    Ruta_Id: int
    Descripcion: Optional[str] = None
    Estatus: Optional[bool] = True

class ContenedorCreate(ContenedorBase):
    pass

class ContenedorUpdate(BaseModel):
    Ubicacion: Optional[str]
    Capacidad: Optional[int]
    Ruta_Id: Optional[int]
    Descripcion: Optional[str]
    Estatus: Optional[bool]
    Fecha_Actualizacion: Optional[datetime]

class ContenedorOut(ContenedorBase):
    ID: int
    Fecha_Registro: datetime
    Fecha_Actualizacion: Optional[datetime]

    class Config:
        orm_mode = True
