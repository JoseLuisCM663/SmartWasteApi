from fastapi import FastAPI
from app.database import engine, Base
from app.routes import usuarios
from app.models.usuarios import Usuario
from app.models.ruta_recoleccion import RutaRecoleccion
from app.models.usuario_ruta import UsuarioRuta
from app.models.contenedor import Contenedor
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8080"],  # permite solo ese origen
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir routers existentes
app.include_router(usuarios.router, prefix="/api/usuarios", tags=["Usuarios"])


# Crear las tablas automáticamente al arrancar la aplicación
@app.on_event("startup")
def crear_tablas():
    Base.metadata.create_all(bind=engine)

