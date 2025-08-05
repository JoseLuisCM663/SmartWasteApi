from sqlalchemy.orm import Session
from datetime import datetime
from app.database import SessionLocal
from app.models.usuarios import Usuario, TipoUsuario
from app.models.ruta_recoleccion import RutaRecoleccion
from app.models.contenedor import Contenedores
from app.models.sensor import Sensor
import bcrypt

def crear_seed():
    db: Session = SessionLocal()

    try:
        # 1. Usuarios
        usuarios = [
            Usuario(
                Tipo_Usuario=TipoUsuario.ADMIN,
                Nombre_Usuario="admin1",
                Correo_Electronico="admin1@smartwaste.com",
                Contrasena=bcrypt.hashpw("admin123".encode('utf-8'), bcrypt.gensalt()).decode('utf-8'),
                Numero_Telefonico_Movil="5551234567",
                Estatus=True,
                Fecha_Registro=datetime.now(),
                Fecha_Actualizacion=datetime.now()
            ),
            Usuario(
                Tipo_Usuario=TipoUsuario.USUARIO,
                Nombre_Usuario="usuario2",
                Correo_Electronico="user2@smartwaste.com",
                Contrasena=bcrypt.hashpw("admin123".encode('utf-8'), bcrypt.gensalt()).decode('utf-8'),
                Numero_Telefonico_Movil="5557654321",
                Estatus=True,
                Fecha_Registro=datetime.now(),
                Fecha_Actualizacion=datetime.now()
            ),
            Usuario(
                Tipo_Usuario=TipoUsuario.CHOFER,
                Nombre_Usuario="chofer1",
                Correo_Electronico="chofer1@smartwaste.com",
                Contrasena=bcrypt.hashpw("admin123".encode('utf-8'), bcrypt.gensalt()).decode('utf-8'),
                Numero_Telefonico_Movil="5559988776",
                Estatus=True,
                Fecha_Registro=datetime.now(),
                Fecha_Actualizacion=datetime.now()
            ),
        ]
        db.add_all(usuarios)
        db.commit()

        # 2. Rutas de recolección
        rutas = [
            RutaRecoleccion(
                Nombre="Ruta Norte",
                Descripcion="Recolección zona norte",
                Fecha_Registro=datetime.now(),
                Fecha_Actualizacion=datetime.now(),
                Estatus=True
            ),
            RutaRecoleccion(
                Nombre="Ruta Centro",
                Descripcion="Recolección zona centro",
                Fecha_Registro=datetime.now(),
                Fecha_Actualizacion=datetime.now(),
                Estatus=True
            )
        ]
        db.add_all(rutas)
        db.commit()

        # 3. Contenedores (asociados a rutas)
        contenedores = [
            Contenedores(
                Ubicacion="Av. Reforma 123, CDMX",
                Capacidad=240,
                Ruta_Id=1,
                Descripcion="Contenedor orgánico",
                Estatus=True,
                Fecha_Registro=datetime.now(),
                Fecha_Actualizacion=datetime.now()
            ),
            Contenedores(
                Ubicacion="Blvd. Hidalgo 456, CDMX",
                Capacidad=360,
                Ruta_Id=2,
                Descripcion="Contenedor inorgánico",
                Estatus=True,
                Fecha_Registro=datetime.now(),
                Fecha_Actualizacion=datetime.now()
            )
        ]
        db.add_all(contenedores)
        db.commit()

        # 4. Sensores (asociados a contenedores)
        sensores = [
            Sensor(
                Tipo="Ultrasonido",
                Descripcion="Sensor de nivel",
                Estatus=True,
                Fecha_Registro=datetime.now(),
                Fecha_Actualizacion=datetime.now(),
                Contenedor_Id=1
            ),
            Sensor(
                Tipo="Peso",
                Descripcion="Sensor de carga",
                Estatus=True,
                Fecha_Registro=datetime.now(),
                Fecha_Actualizacion=datetime.now(),
                Contenedor_Id=2
            )
        ]
        db.add_all(sensores)
        db.commit()

        print("✅ Datos de prueba insertados correctamente.")
    except Exception as e:
        db.rollback()
        print(f"❌ Error al insertar datos: {e}")
    finally:
        db.close()


if __name__ == "__main__":
    crear_seed()
