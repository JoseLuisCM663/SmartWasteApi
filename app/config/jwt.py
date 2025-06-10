from datetime import datetime, timedelta
from jose import JWTError, jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from app.models.usuarios import Usuario
from app.database import get_db
from typing import Optional
from dotenv import load_dotenv
import os

# Cargar las variables de entorno desde el archivo .env
load_dotenv()

# Configuración de JWT
SECRET_KEY = os.getenv("SECRET_KEY")  # Clave secreta para firmar el token
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = 30  # Duración del token

# Esquema de seguridad para JWT
security = HTTPBearer()  # Usamos HTTPBearer en lugar de OAuth2PasswordBearer

# Función para crear tokens JWT
def crear_token_acceso(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# Función para obtener el usuario actual basado en el token JWT
def obtener_usuario_actual(
    credentials: HTTPAuthorizationCredentials = Depends(security),  # Extrae el token de la cabecera
    db: Session = Depends(get_db)  # Inyecta la sesión de la base de datos
) -> Usuario:
    # Excepción para credenciales inválidas
    credenciales_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="No se pudo validar el token",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        # Extraer el token de las credenciales
        token = credentials.credentials
        print(f"Token recibido: {token}")  # Depuración: Imprime el token

        # Decodificar el token
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        print(f"Payload decodificado: {payload}")  # Depuración: Imprime el payload

        # Obtener el correo electrónico del payload
        correo_electronico: str = payload.get("sub")
        if correo_electronico is None:
            raise credenciales_exception
    except JWTError as e:
        print(f"Error al decodificar el token: {e}")  # Depuración: Imprime el error
        raise credenciales_exception

    # Buscar al usuario en la base de datos
    usuario = db.query(Usuario).filter(Usuario.Correo_Electronico == correo_electronico).first()
    if usuario is None:
        raise credenciales_exception

    return usuario