from sqlalchemy.orm import Session
from app.models.usuarios import Usuario
from app.schemas.usuarios import UsuarioCreate
from passlib.context import CryptContext
from datetime import datetime
from fastapi import HTTPException, status


# Configuración para el hashing de contraseñas
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Función para hashear la contraseña
def hash_contrasena(contrasena: str):
    return pwd_context.hash(contrasena)

# Función para crear un nuevo usuario
def crear_usuario(db: Session, usuario: UsuarioCreate):
    # Verificar si el correo ya está registrado
    db_usuario = db.query(Usuario).filter(
        (Usuario.Correo_Electronico == usuario.Correo_Electronico) | 
        (Usuario.Nombre_Usuario == usuario.Nombre_Usuario)
    ).first()
    if db_usuario:
        return None  # El correo o el nombre de usuario ya están registrados

    # Validar que la contraseña tenga al menos 8 caracteres
    if len(usuario.Contrasena) < 8:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="La contraseña debe tener al menos 8 caracteres",
        )
    # Crear el nuevo usuario
    nuevo_usuario = Usuario(
        Nombre_Usuario=usuario.Nombre_Usuario,
        Tipo_Usuario=usuario.Tipo_Usuario,
        Correo_Electronico=usuario.Correo_Electronico,
        Contrasena=hash_contrasena(usuario.Contrasena),
        Numero_Telefonico_Movil=usuario.Numero_Telefonico_Movil,
        Estatus=usuario.Estatus,
        Fecha_Registro=datetime.now(),  # Establecer la fecha de registro actual
        Fecha_Actualizacion=datetime.now(),  # Establecer la fecha de actualización actual
    )
    db.add(nuevo_usuario)
    db.commit()
    db.refresh(nuevo_usuario)
    return nuevo_usuario

# Función para verificar la contraseña
def verificar_contrasena(contrasena_plana: str, contrasena_hasheada: str):
    return pwd_context.verify(contrasena_plana, contrasena_hasheada)

# Función para autenticar al usuario
def autenticar_usuario(db: Session, username: str, password: str):
    # Buscar al usuario por correo electrónico
    usuario = db.query(Usuario).filter(Usuario.Correo_Electronico == username).first()
    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Correo electrónico o contraseña incorrectos",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Verificar la contraseña
    if not verificar_contrasena(password, usuario.Contrasena):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Correo electrónico o contraseña incorrectos",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return usuario

# Función para obtener un usuario por su ID
def obtener_usuario_por_id(db: Session, usuario_id: int):
    """
    Obtener un usuario por su ID.
    """
    return db.query(Usuario).filter(Usuario.ID == usuario_id).first()

# Función para obtener actualizar un usuario por su ID
def update_usuario(db: Session, usuario_id: int, usuario_data: UsuarioCreate):
    """
    Actualizar un usuario existente.
    """
    usuario = db.query(Usuario).filter(Usuario.ID == usuario_id).first()
    if not usuario:
        return None

    # Verificar si el correo o nombre de usuario ya están registrados
    if usuario_data.Correo_Electronico != usuario.Correo_Electronico:
        db_usuario = db.query(Usuario).filter(Usuario.Correo_Electronico == usuario_data.Correo_Electronico).first()
        if db_usuario:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El correo electrónico ya está registrado",
            )
    
    if usuario_data.Nombre_Usuario != usuario.Nombre_Usuario:
        db_usuario = db.query(Usuario).filter(Usuario.Nombre_Usuario == usuario_data.Nombre_Usuario).first()
        if db_usuario:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El nombre de usuario ya está registrado",
            )
    
    # Validar que la nueva contraseña tenga al menos 8 caracteres
    if 'Contrasena' in usuario_data.dict(exclude_unset=True) and len(usuario_data.Contrasena) < 8:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="La contraseña debe tener al menos 8 caracteres",
        )

    # Actualizar los datos del usuario
    for key, value in usuario_data.dict(exclude_unset=True).items():
        setattr(usuario, key, value)

    # Si se actualizó la contraseña, la hasheamos
    if 'Contrasena' in usuario_data.dict(exclude_unset=True):
        usuario.Contrasena = hash_contrasena(usuario_data.Contrasena)

    usuario.Fecha_Actualizacion = datetime.now()  # Actualizar la fecha de modificación
    db.commit()
    db.refresh(usuario)
    return usuario

def eliminar_usuario(db: Session, usuario_id: int):
    """
    Eliminar un usuario por su ID.
    """
    usuario = db.query(Usuario).filter(Usuario.ID == usuario_id).first()
    if not usuario:
        return None

    db.delete(usuario)
    db.commit()
    return usuario

def obtener_usuarios(db: Session, skip: int = 0, limit: int = 100):
    """
    Obtener una lista de usuarios con paginación.
    """
    return db.query(Usuario).offset(skip).limit(limit).all()
    