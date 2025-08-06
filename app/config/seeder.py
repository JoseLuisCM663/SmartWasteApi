"""
Seeder de datos para SmartWasteApi
-----------------------------------
Este script inserta datos de prueba en la base de datos:
- Usuarios (Admin, Usuario, Chofer)
- Rutas
- Contenedores (asociados a rutas)
- Sensores (asociados a contenedores)

Uso:
    python config/seeder.py --usuarios 3 --rutas 2 --contenedores 2 --sensores 2 --seed 42
"""

from sqlalchemy.orm import Session
from datetime import datetime
from app.database import SessionLocal
from app.models.usuarios import Usuario, TipoUsuario
from app.models.ruta_recoleccion import RutaRecoleccion
from app.models.contenedor import Contenedores
from app.models.sensor import Sensor
from app.models.lectura_sensor import LecturaSensor
from app.models.bitacora_contenedor import BitacoraContenedor
from app.models.bitacora_recolecion import BitacoraRecoleccion
import bcrypt
import random
import argparse
from faker import Faker
import itertools

fake = Faker()

def crear_seed(n_usuarios, n_rutas, n_contenedores, n_sensores, seed=None):
    if seed:
        Faker.seed(seed)
        random.seed(seed)

    db: Session = SessionLocal()

    try:
        # Limpieza previa
        db.query(LecturaSensor).delete()
        db.query(BitacoraContenedor).delete()
        db.query(BitacoraRecoleccion).delete()
        db.query(Sensor).delete()
        db.query(Contenedores).delete()
        db.query(RutaRecoleccion).delete()
        db.query(Usuario).delete()

        db.commit()


        # 1. Usuarios
        tipos = [TipoUsuario.ADMIN, TipoUsuario.USUARIO, TipoUsuario.CHOFER]
        usuarios = []
        for i in range(n_usuarios):
            usuarios.append(Usuario(
                Tipo_Usuario=random.choice(tipos),
                Nombre_Usuario=fake.user_name(),
                Correo_Electronico=fake.email(),
                Contrasena=bcrypt.hashpw("admin123".encode('utf-8'), bcrypt.gensalt()).decode('utf-8'),
                Numero_Telefonico_Movil=fake.msisdn()[:10],
                Estatus=True,
                Fecha_Registro=datetime.now(),
                Fecha_Actualizacion=datetime.now()
            ))
        db.add_all(usuarios)
        db.commit()

        # 2. Rutas
        rutas = []
        for i in range(n_rutas):
            rutas.append(RutaRecoleccion(
                Nombre=f"Ruta {fake.city_suffix()}",
                Descripcion=f"Recolección en {fake.city()}",
                Fecha_Registro=datetime.now(),
                Fecha_Actualizacion=datetime.now(),
                Estatus=True
            ))
        db.add_all(rutas)
        db.commit()

        # 3. Contenedores

        # Obtener rutas existentes en base de datos
        rutas_disponibles = db.query(RutaRecoleccion).all()
        ids_rutas = [ruta.ID for ruta in rutas_disponibles]

        # Ciclo infinito de IDs de rutas disponibles
        id_ciclico = itertools.cycle(ids_rutas)

        contenedores = []
        for i in range(n_contenedores):
            contenedores.append(Contenedores(
                Ubicacion=fake.address(),
                Capacidad=random.choice([240, 360, 120]),
                Ruta_Id=next(id_ciclico),  # ✅ Siempre usa un ID válido
                Descripcion=random.choice(["Orgánico", "Inorgánico", "Mixto"]),
                Estatus=True,
                Fecha_Registro=datetime.now(),
                Fecha_Actualizacion=datetime.now()
            ))
        db.add_all(contenedores)
        db.commit()

        
        # 4. Sensores

        # Obtener contenedores existentes en base de datos
        contenedores_existentes = db.query(Contenedores).all()
        ids_contenedores = [contenedor.ID for contenedor in contenedores_existentes]

        # Crear ciclo infinito de IDs de contenedores
        id_contenedor_ciclico = itertools.cycle(ids_contenedores)

        tipos_sensores = ["Ultrasonido", "Peso", "Temperatura"]

        lista_sensores = []
        for i in range(n_sensores):
            nuevo_sensor = Sensor(
                Tipo=random.choice(tipos_sensores),
                Descripcion="Sensor para medición de nivel o peso",
                Estatus=True,
                Fecha_Registro=datetime.now(),
                Fecha_Actualizacion=datetime.now(),
                Contenedor_Id=next(id_contenedor_ciclico)  # Asignar ID válido cíclicamente
            )
            lista_sensores.append(nuevo_sensor)

        db.add_all(lista_sensores)
        db.commit()

        print("✅ Datos de prueba insertados correctamente.")

    except Exception as e:
        db.rollback()
        print(f"❌ Error al insertar datos: {e}")
    finally:
        db.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Seeder para SmartWasteApi")
    parser.add_argument("--usuarios", type=int, default=3, help="Cantidad de usuarios")
    parser.add_argument("--rutas", type=int, default=2, help="Cantidad de rutas")
    parser.add_argument("--contenedores", type=int, default=2, help="Cantidad de contenedores")
    parser.add_argument("--sensores", type=int, default=2, help="Cantidad de sensores")
    parser.add_argument("--seed", type=int, help="Semilla para aleatoriedad reproducible")
    args = parser.parse_args()

    crear_seed(
        n_usuarios=args.usuarios,
        n_rutas=args.rutas,
        n_contenedores=args.contenedores,
        n_sensores=args.sensores,
        seed=args.seed
    )
