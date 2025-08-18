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

# Modelo de Análisis Supervisado (ML) - Clasificación de Rutas

Este módulo implementa un **modelo supervisado** para clasificar rutas de recolección como **Eficientes** o **Ineficientes**, utilizando datos históricos de bitácoras de recolección y contenedores.

---

## Estructura de la API

Se exponen los siguientes endpoints en FastAPI:

### Entrenamiento del modelo

```
POST /ml/entrenar/
```

**Descripción:**
Entrena un modelo de clasificación usando los CSV de bitácoras de recolección y contenedores.

**Código de ejemplo:**

```python
resultado = ml_model.entrenar_modelo_bitacoras(
    "datos/bitacora_recoleccion_etl.csv",
    "datos/bitacora_contenedor_etl.csv"
)
```

**Respuesta esperada:**

```json
{
  "mensaje": "Modelo entrenado y guardado",
  "accuracy": 0.85,
  "f1_score": 0.84,
  "reporte": "Classification report completo..."
}
```

---

### Predicción de rutas

```
GET /ml/predecir/?bitacora_id={id}
```

**Descripción:**
Predice si una ruta de recolección (bitácora) es **Eficiente** o **Ineficiente**, usando los datos de BitacoraRecoleccion y BitacoraContenedor.

**Código de ejemplo:**

```python
resultado = ml_model.predecir_ruta_por_bitacora(bitacora_id, db)
```

**Respuesta esperada:**

```json
{
  "bitacora_id": 123,
  "prediccion": "Eficiente",
  "features": {
    "Tiempo_Duracion": 90,
    "Cantidad_Contenedores": 5,
    "Porcentaje_Llenado": 0.85,
    "Recolectado": 1.0
  }
}
```

---

## Proceso de Entrenamiento

1. **Carga de datos:** Se leen los archivos CSV de bitácoras de recolección y contenedores.
2. **Preprocesamiento:**

   * Conversión de fechas.
   * Agregación de métricas por ruta: promedio de llenado y recolectado.
3. **Definición de etiqueta (target):**

   * `Eficiente` (1): `Tiempo_Duracion <= 100` y `Recolectado >= 0.8`
   * `Ineficiente` (0): caso contrario
4. **Selección de features:**

   * `Tiempo_Duracion`
   * `Cantidad_Contenedores`
   * `Porcentaje_Llenado`
   * `Recolectado`
5. **Split Train/Test:** 70% entrenamiento, 30% prueba.
6. **Modelo:** RandomForestClassifier con 100 estimadores.
7. **Evaluación:**

   * Accuracy
   * F1-score
   * Classification report
8. **Guardado del modelo:** `datos/modelos/modelo_rutas.pkl`

---

## Métricas de Evaluación

* **Accuracy:** Porcentaje de predicciones correctas sobre el total.
* **F1-score:** Media armónica entre precisión y recall.
* **Classification Report:** Desglose de precisión, recall y F1-score por clase.

---

## Dependencias

* `pandas`
* `numpy`
* `scikit-learn`
* `joblib`
* `fastapi`
* `sqlalchemy`

---

## Uso en FastAPI


Después de incluir el router, se pueden usar los endpoints `/ml/entrenar/` y `/ml/predecir/`.

---

**Proyecto:** SmartWasteApi
