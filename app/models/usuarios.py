from sqlalchemy import Column, Integer, String, Boolean, DateTime
from app.database import Base
from sqlalchemy import Column, Integer, String, DateTime, Boolean as SQLEnum
from app.schemas.usuarios import TipoUsuario  # Enum que creaste con str y Enum

class Usuario(Base):
    __tablename__ = "tbb_usuarios"
    
    ID = Column(Integer, primary_key=True, autoincrement=True, index=True)
    Tipo_Usuario = Column(SQLEnum(TipoUsuario, name="tipo_usuario_enum"), default=TipoUsuario.USUARIO)
    Nombre_Usuario = Column(String(50), unique=True, index=True)
    Correo_Electronico = Column(String(100), unique=True, index=True)
    Contrasena = Column(String(255))
    Numero_Telefonico_Movil = Column(String(20))
    Estatus = Column(Boolean, default=True)
    Fecha_Registro = Column(DateTime)
    Fecha_Actualizacion = Column(DateTime)

