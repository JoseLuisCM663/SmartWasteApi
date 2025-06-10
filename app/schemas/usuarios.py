from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from enum import Enum


# ✅ Heredamos de str y Enum para que funcione bien con Pydantic
class TipoUsuario(str, Enum):
    ADMIN = "Administrador"
    USUARIO = "Usuario"
    CHOFER = "Chofer"

class UsuarioBase(BaseModel):
    Nombre_Usuario: str
    Correo_Electronico: str
    Numero_Telefonico_Movil: Optional[str] = None
    Tipo_Usuario: Optional[TipoUsuario] = TipoUsuario.USUARIO  # Valor por defecto

class UsuarioCreate(UsuarioBase):
    Contrasena: str
    Estatus: Optional[str] = "Activo"  # Valor por defecto

class UsuarioResponse(UsuarioBase):
    ID: int
    Estatus: str
    Fecha_Registro: datetime
    Fecha_Actualizacion: datetime

    class Config:
        orm_mode = True

class LoginRequest(BaseModel):
    Correo_Electronico: str
    Contrasena: str
