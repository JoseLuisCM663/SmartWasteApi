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
#  Seeder de Datos

Este repositorio incluye scripts para poblar la base de datos de **SmartWasteAPI** con datos de prueba.

---

## 🚀 Funcionalidades incluidas

### 1. Seeder principal (`config/seeder.py`)

Este script inserta datos iniciales en las siguientes tablas:

- ✅ **Usuarios** (Admin, Usuario, Chofer)
- ✅ **Rutas** de recolección
- ✅ **Contenedores** (asociados a rutas)
- ✅ **Sensores** (asociados a contenedores)
- ✅ **Relación Usuario-Ruta**

#### ▶️ Uso

```bash
python config/seeder.py --usuarios 3 --rutas 2 --contenedores 2 --sensores 2 --seed 42
```

#### 📌 Argumentos

| Parámetro        | Descripción                               | Valor por defecto |
|------------------|--------------------------------------------|-------------------|
| `--usuarios`     | Número de usuarios a crear                 | 3                 |
| `--rutas`        | Número de rutas                            | 2                 |
| `--contenedores` | Número de contenedores                     | 2                 |
| `--sensores`     | Número de sensores                         | 2                 |
| `--seed`         | Semilla para datos aleatorios reproducibles | Opcional          |

---

### 2. Generador de Lecturas de Sensor

Genera lecturas simuladas para sensores.

#### 🧪 Uso

```python
from crud.seeder import generar_lecturas_sensor

generar_lecturas_sensor(sensor_id=1, cantidad=100, valor_min=10, valor_max=90)
```

#### 🔧 Parámetros

- `sensor_id`: ID del sensor a asociar las lecturas
- `cantidad`: Número de lecturas a generar
- `valor_min`: Valor mínimo de lectura
- `valor_max`: Valor máximo de lectura
- `intervalo_minutos`: (opcional) intervalo entre lecturas

---

### 3. Generador de Bitácoras de Recolección

Inserta bitácoras con datos asociados a rutas y contenedores.

#### 🧾 Uso

```python
from crud.seeder import poblar_bitacoras
from app.database import SessionLocal

db = SessionLocal()
poblar_bitacoras(db, cantidad=10)
```

---

## 🗂 Estructura de Carpetas

```
config/
  └── seeder.py           # Seeder principal
crud/
  └── seeder.py           # Funciones de utilidad (lecturas, bitácoras)
```
# 🧹 Preprocesamiento y Limpieza de Datos - SmartWasteApi

Este módulo forma parte del backend de **SmartWasteApi**, encargado del **ETL (Extracción, Transformación y Carga)** de datos recolectados por sensores y bitácoras del sistema de gestión inteligente de residuos.

## 📂 Funcionalidades implementadas

### 1. `exportar_lecturas_sensor(sensor_id, ruta_csv, db)`

Exporta las lecturas de un sensor específico a un archivo CSV, siguiendo los pasos del proceso ETL:

- **Extracción:** Consultas a la base de datos con SQLAlchemy por `Sensor_Id`.
- **Transformación:** Se aplican técnicas de:
  - Conversión y ordenación temporal (`datetime`)
  - Eliminación de duplicados
  - Filtrado y clipping de valores (0-100)
  - Resampleo a intervalos regulares (5 minutos)
  - Interpolación lineal para valores faltantes
  - Redondeo de valores
  - Creación de variables adicionales: `Hora`, `Día de la semana`
- **Carga:** Generación y guardado de un archivo `.csv` limpio y estructurado.

### 2. `etl_bitacoras(db)`

Realiza la limpieza y exportación de datos de dos tablas de bitácoras:

- **Bitácora de Recolección:**
  - Se excluyen registros sin fecha o ruta válida
  - Se filtran valores atípicos en duración (>500)
  - Se imputan valores por defecto para campos nulos (ej. observaciones)
- **Bitácora de Contenedor:**
  - Se validan fechas y IDs de contenedores
  - Se eliminan valores de porcentaje de llenado fuera de rango (0-100)
  - Se etiquetan estados desconocidos

Retorna dos `DataFrames` limpios listos para análisis o exportación.

## 🚀 Endpoints disponibles

### `GET /exportar-sensor/?sensor_id=ID`

- Ejecuta `exportar_lecturas_sensor`
- Devuelve un archivo `.csv` limpio con las lecturas del sensor especificado

### `GET /exportar-bitacoras/`

- Ejecuta `etl_bitacoras`
- Devuelve un archivo `.zip` con los siguientes CSVs:
  - `bitacora_recoleccion_etl.csv`
  - `bitacora_contenedor_etl.csv`

## 📌 Ubicación del código

- Lógica principal de ETL: `app/utils/etl_export.py`
- Rutas de exportación: `app/routers/exportar.py`

## 🛠 Requisitos

- Pandas
- Numpy
- SQLAlchemy
- FastAPI
- Zipfile (módulo estándar de Python)

## 📁 Ejemplo de uso

```bash
curl -X GET "http://localhost:8000/exportar-sensor/?sensor_id=1" -o lecturas_sensor_1.csv

curl -X GET "http://localhost:8000/exportar-bitacoras/" -o bitacoras_etl.zip
```

## 📈 Objetivo del módulo

Garantizar datos limpios, consistentes y listos para análisis de comportamiento, modelos predictivos o visualizaciones, reduciendo errores por datos atípicos o faltantes.

---
**Desarrollado por José Luis Campos Márquez**
