from fastapi import FastAPI
from app.database import engine, Base
from app.routes import contenedor
from app.routes import usuarios
from app.routes import ruta_recolecion
from app.routes import sensor
from app.routes import lectura_sensor
from app.routes import usuario_ruta
from app.routes import seder
from app.routes import etl_exportar
from app.routes import ml
from app.routes import ml_unsupervided
from app.routes import dw_etl 
from app.models import bitacora_contenedor
from app.models import bitacora_recolecion
from app.config.seeder import crear_seed  # ✅ Importación del seeder
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8080"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir routers
app.include_router(usuarios.router, prefix="/api/usuarios")
app.include_router(contenedor.router_contenedor, prefix="/api/contenedores")
app.include_router(ruta_recolecion.router_ruta, prefix="/api/rutas_recoleccion")
app.include_router(sensor.router_sensor, prefix="/api/sensores")
app.include_router(lectura_sensor.router_lectura_sensor, prefix="/api/lecturas_sensor")
app.include_router(usuario_ruta.router_usuario_ruta, prefix="/api/usuario_ruta")
app.include_router(seder.router_seeder, prefix="/api")
app.include_router(etl_exportar.router_exportar, prefix="/api/exportar", tags=["Exportaciones"])
app.include_router(ml.router_ml, prefix="/api/ml", tags=["Machine Learning"])
app.include_router(ml_unsupervided.router_ml, prefix="/api/ml_unsupervised", tags=["Machine Learning No Supervisado"])
app.include_router(dw_etl.router_dw, prefix="/api/dw", tags=["Data Warehouse"])
# Crear tablas
@app.on_event("startup")
def crear_tablas():
    Base.metadata.create_all(bind=engine)



# Ejecutar seeder automáticamente al iniciar la app
@app.on_event("startup")
def ejecutar_seeder():
    crear_seed(
        n_usuarios=3,
        n_rutas=4,
        n_contenedores=5,
        n_sensores=10,
        seed=42
    )

with engine.connect() as conn:
    # Abrir el archivo en UTF-8
    with open("app/utils/dw_schema.sql", "r", encoding="utf-8") as f:
        sql_commands = f.read()
    for command in sql_commands.split(";"):
        if command.strip():
            conn.execute(text(command))
    conn.commit()

print("✅ Tablas del DW creadas correctamente.")
