from fastapi import FastAPI
from app.database import engine, Base
from app.routes import contenedor
from app.routes import usuarios
from app.routes import ruta_recolecion
from app.routes import sensor
from app.routes import lectura_sensor
from app.models.usuarios import Usuario
from app.models.ruta_recoleccion import RutaRecoleccion
from app.models.usuario_ruta import UsuarioRuta
from app.models.contenedor import Contenedores
from app.models.sensor import Sensor
from app.models.lectura_sensor import LecturaSensor
from app.models.bitacora_recolecion import BitacoraRecoleccion
from app.models.bitacora_contenedor import BitacoraContenedor
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
app.include_router(usuarios.router, prefix="/api/usuarios")
app.include_router(contenedor.router_contenedor, prefix="/api/contenedores")
app.include_router(ruta_recolecion.router_ruta, prefix="/api/rutas_recoleccion")
app.include_router(sensor.router_sensor, prefix="/api/sensores")
app.include_router(lectura_sensor.router_lectura_sensor, prefix="/api/lecturas_sensor")

# Crear las tablas automáticamente al arrancar la aplicación
@app.on_event("startup")
def crear_tablas():
    Base.metadata.create_all(bind=engine)


