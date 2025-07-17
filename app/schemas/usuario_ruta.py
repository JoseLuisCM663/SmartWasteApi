from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class UsuarioRutaBase(BaseModel):
    Usuario_Id: int
    Ruta_Id: int
    Fecha_Registro: datetime
    Fecha_Actualizacion: Optional[datetime] = None
    Estatus: Optional[bool] = True

class UsuarioRutaCreate(UsuarioRutaBase):
    ID: Optional[int] = None
    pass

class UsuarioRutaUpdate(BaseModel):
    Usuario_Id: int
    Ruta_Id: int
    Fecha_Actualizacion: Optional[datetime] = None
    Estatus: Optional[bool] = True

class UsuarioRutaResponse(UsuarioRutaBase):
    model_config = {
        "from_attributes": True
    }

