import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session

# Cargar variables de entorno
load_dotenv()

# Datos de conexión
DB_USERNAME = os.getenv("DB_USERNAME")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")

# Construir URL
if all([DB_USERNAME, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME]):
    SQLALCHEMY_DATABASE_URL = f"mysql+pymysql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    print("✅ Conectado a la base de datos MySQL")
else:
    SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
    print("⚠️ Variables de entorno no detectadas. Usando base de datos SQLite temporal (modo CI/CD).")

# 🔹 Nueva variable que indica si estamos usando SQLite
is_sqlite = SQLALCHEMY_DATABASE_URL.startswith("sqlite")

# Crear el motor
if is_sqlite:
    engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
else:
    engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"charset": "utf8mb4"})

# Sesión
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Función para obtener la sesión
def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
