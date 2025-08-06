# 📦 SmartWaste API

**Sistema de gestión inteligente de residuos urbanos**  
Este backend basado en FastAPI permite gestionar usuarios, sensores, contenedores, rutas y lecturas para optimizar la recolección de residuos urbanos mediante IoT.

---

## 🚀 Clonación y Ejecución del Proyecto

### 🔧 Requisitos previos

- Python 3.10 o superior  
- MySQL instalado y corriendo (o Docker para usar el contenedor)  
- Git  
- pip/venv o [Poetry](https://python-poetry.org/) (recomendado)

---

### 📥 Clonar el repositorio

```bash
git clone https://github.com/JoseLuisCM663/SmartWasteApi.git
cd SmartWasteApi
```

---

### 🐍 Configurar entorno virtual (opcional pero recomendado)

**Con `venv`:**

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

---

### 📦 Instalar dependencias

**Con pip:**

```bash
pip install -r requirements.txt
```

---

### ⚙️ Configuración del entorno

Copiar archivo `.env.example` a `.env`:

```bash
cp .env.example .env
```

Modificar las variables en el archivo `.env`:

```env
DB_USERNAME=root
DB_PASSWORD=12345678
DB_HOST=localhost
DB_PORT=3306
DB_NAME=smartwaste
SECRET_KEY=ejemplo
ALGORITHM=HS256
```

---

### 🛢️ Configurar base de datos

1. Crear base de datos:

```sql
CREATE DATABASE smartwaste;
```

---

### 🚀 Ejecutar la aplicación

```bash
uvicorn app.main:app --reload
```

La aplicación estará disponible en:  
➡️ [http://localhost:8000](http://localhost:8000)

---

### 🐳 Ejecución con Docker

Construir y ejecutar los contenedores:

```bash
docker-compose up --build
```

La aplicación estará disponible en:  
➡️ [http://localhost:8000](http://localhost:8000)

---

## 📚 Documentación de la API

- Swagger UI: [http://localhost:8000/docs](http://localhost:8000/docs)  
- Redoc: [http://localhost:8000/redoc](http://localhost:8000/redoc)


---

## 🛠️ Estructura del Proyecto

```
app/
├── config/        # Configuraciones principales
├── crud/          # Operaciones CRUD para la base de datos
├── models/        # Modelos de SQLAlchemy
├── schemas/       # Esquemas Pydantic para validación
├── routes/        # Endpoints para acceso a las funciones
├── utils/         # 
├── main.py         # Rutas principales
└── database.py    # Configuración de la base de datos
```

---

**Desarrollado por José Luis Campos Márquez**