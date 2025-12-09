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
    "public/bitacora_recoleccion_etl.csv",
    "public/bitacora_contenedor_etl.csv"
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
8. **Guardado del modelo:** `public/modelos/modelo_rutas.pkl`

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
# Modelo de Análisis No Supervisado (ML)

## Objetivo

Implementar un **modelo de análisis no supervisado** sobre los datos de lecturas de sensores para identificar patrones o agrupaciones naturales. En este proyecto se utilizó **K-Means Clustering** como técnica principal.

---

## Metodología

1. **Preparación de datos**

   * Se utiliza el CSV generado previamente con todas las lecturas de sensores (`lecturas_todos_sensores.csv`).
   * Columnas consideradas: `Valor`, `Hora`, `DiaSemana`.
   * Se transforma `DiaSemana` a valores numéricos (`0=Monday, 6=Sunday`).
   * Se escalan las variables usando `StandardScaler` para que todas tengan la misma importancia en el clustering.

2. **Entrenamiento del modelo**

   * Se utiliza `KMeans` de `sklearn` con número de clusters configurable (`n_clusters`).
   * El modelo se ajusta a los datos escalados y se asigna un cluster a cada lectura.
   * El modelo entrenado se guarda en: `datos/modelos/kmeans_model.pkl`.

3. **Generación de informe**

   * Se genera un **PDF** que incluye:

     * Silhouette Score para evaluar la calidad del clustering.
     * Gráficos 2D de:

       * Valor vs Hora
       * Valor vs Día de la semana
     * Tabla con los promedios de cada variable por cluster.
     * Interpretación automática en texto para cada cluster, explicando sus características de manera comprensible para un usuario común.

---

## Métricas utilizadas

* **Silhouette Score**: Indica qué tan separados y compactos están los clusters.

  * Valor cercano a 1: clusters bien definidos.
  * Valor cercano a 0: clusters solapados o poco definidos.
  * Valor negativo: posibles errores en la asignación de clusters.

* **Estadísticas por cluster**:

  * Cantidad de lecturas por cluster.
  * Promedio de `Valor`, `Hora` y `DiaSemana_num` por cluster.

---

## Interpretación

Cada cluster representa un **patrón de comportamiento de lecturas**. Por ejemplo:

* Cluster 0: lecturas con valores altos en horas pico.
* Cluster 1: lecturas bajas en días específicos de la semana.
* Cluster 2: lecturas promedio distribuidas de manera uniforme.

> Nota: La interpretación se genera automáticamente en el PDF para facilitar su comprensión por cualquier usuario.

---

## Archivos generados

* Modelo entrenado: `public/modelos/kmeans_model.pkl`
* Informe PDF: `public/informe_clusters.pdf`

---

## Uso en FastAPI

Existen endpoints para entrenar el modelo y descargar el PDF:

1. **Entrenar modelo y generar PDF**

```
GET /ml_unsupervised/entrenar/?n_clusters=3
```

2. **Descargar PDF**

```
GET /ml_unsupervised/descargar-informe/
```

---

## Bibliotecas utilizadas

* `pandas`
* `matplotlib`
* `sklearn` (`KMeans`, `StandardScaler`, `silhouette_score`)
* `joblib`
* `reportlab`

# 📊 Modelo de Data Warehouse
---

En esta fase se diseñó el **Modelo de Data Warehouse** del proyecto **SmartWasteApi**, siguiendo un **esquema en estrella** para facilitar la integración, consulta y análisis de la información histórica de las lecturas de los sensores de residuos.

---

## 🏗️ Esquema en Estrella

El modelo se compone de una **tabla de hechos central** (`Fact_Lecturas`) y varias **tablas de dimensiones** relacionadas.  

### 🔹 Tabla de Hechos: `Fact_Lecturas`
Contiene los datos medibles del sistema, provenientes de las lecturas de los sensores.

| Campo          | Tipo        | Descripción |
|----------------|------------|-------------|
| **Lectura_ID** | INT (PK)   | Identificador único de la lectura |
| **Sensor_Id**  | INT (FK)   | Clave foránea hacia `Dim_Sensor` |
| **Contenedor_Id** | INT (FK) | Clave foránea hacia `Dim_Contenedor` |
| **Ruta_Id**    | INT (FK)   | Clave foránea hacia `Dim_Ruta` |
| **Tiempo_ID**  | INT (FK)   | Clave foránea hacia `Dim_Tiempo` |
| **Valor**      | FLOAT      | Medición registrada (nivel de llenado del contenedor en %) |

---

### 🔹 Dimensiones

#### `Dim_Sensor`
Información sobre los sensores que capturan las lecturas.

| Campo       | Tipo        | Descripción |
|-------------|------------|-------------|
| **Sensor_Id** | INT (PK) | Identificador único del sensor |
| Tipo        | VARCHAR    | Tipo de sensor (ultrasónico, presión, etc.) |
| Modelo      | VARCHAR    | Modelo o referencia del fabricante |

---

#### `Dim_Contenedor`
Describe los contenedores de residuos.

| Campo             | Tipo        | Descripción |
|-------------------|------------|-------------|
| **Contenedor_Id** | INT (PK)   | Identificador único del contenedor |
| Ubicacion         | VARCHAR    | Dirección o zona del contenedor |
| Capacidad         | FLOAT      | Capacidad máxima en litros |

---

#### `Dim_Ruta`
Información sobre las rutas de recolección.

| Campo        | Tipo        | Descripción |
|--------------|------------|-------------|
| **Ruta_Id**  | INT (PK)   | Identificador único de la ruta |
| Nombre       | VARCHAR    | Nombre de la ruta |
| Descripción  | VARCHAR    | Observaciones adicionales |

---

#### `Dim_Tiempo`
Dimensión temporal para análisis histórico.

| Campo         | Tipo        | Descripción |
|---------------|------------|-------------|
| **Tiempo_ID** | INT (PK)   | Identificador único del tiempo |
| Fecha         | DATE       | Fecha de la lectura |
| Hora          | TIME       | Hora de la lectura |
| Dia           | INT        | Día del mes |
| Mes           | INT        | Mes |
| Año           | INT        | Año |
| DiaSemana     | VARCHAR    | Nombre del día (Lunes, Martes, etc.) |

---

## 📐 Jerarquías Definidas

1. **Tiempo** → Año > Mes > Día > Hora  
2. **Ruta** → Ruta > Contenedor > Sensor  

Estas jerarquías permiten realizar análisis agregados por periodo, ubicación y dispositivo.

---

## 📑 Metadatos

- **Grano del Data Warehouse**: Cada registro en `Fact_Lecturas` representa una **lectura puntual de un sensor en un contenedor en un instante de tiempo específico**.  
- **Integración**: Las dimensiones se mantienen independientes para permitir la extensibilidad del modelo (por ejemplo, agregar nuevas rutas o sensores sin rediseñar el esquema).  
- **Optimización**: El esquema en estrella se eligió por su simplicidad y eficiencia para consultas OLAP.  

---

✅ Con este modelo, el Data Warehouse soporta análisis de llenado de contenedores, eficiencia de rutas y comportamiento temporal de los residuos.

# 📊 Visualización y Dashboard

## 📝 Descripción
En este módulo se implementó un **dashboard interactivo** utilizando **Streamlit** y **Plotly**, con el objetivo de analizar los datos de:
- **Bitácora de Recolección**
- **Bitácora de Contenedores**
- **Lecturas de Sensores**

La visualización permite al usuario explorar, comparar y detectar patrones clave en las operaciones del sistema de recolección de residuos inteligentes.

---

## 🎯 Objetivo
- Facilitar el **análisis visual** de los datos recolectados.
- Identificar **tendencias y anomalías** en los tiempos de recolección, llenado de contenedores y lecturas de sensores.
- Apoyar la **toma de decisiones** en la planeación de rutas y mantenimiento de contenedores.

---

## ⚙️ Herramientas utilizadas
- **Streamlit** → Framework para construir el dashboard interactivo.  
- **Plotly Express** → Librería de visualización interactiva para gráficos dinámicos.  
- **Pandas** → Manipulación y limpieza de datos antes de la visualización.  

---

## 📂 Estructura de Archivos
dashboard/
│── dashboard.py # Código principal del dashboard
│── datos/
├── bitacora_recoleccion_etl.csv
├── bitacora_contenedor_etl.csv
├── lecturas_todos_sensores.csv

---

## 📺 Visualizaciones Implementadas

### 1. 📦 Bitácora de Contenedores
- **Histograma del porcentaje de llenado** → distribuciones por rango.  
- **Tendencias temporales** → evolución del llenado por fecha.  
- **Boxplot por estado del contenedor** → identificación de outliers.  

### 2. 🚛 Bitácora de Recolección
- **Duración promedio de rutas** → análisis de eficiencia.  
- **Cantidad de contenedores recolectados por ruta** → carga de trabajo.  
- **Comparación de observaciones** → patrones de incidencias.  

### 3. 📡 Lecturas de Sensores
- **Serie temporal de valores por sensor** → evolución en el tiempo.  
- **Promedios por día de la semana** → patrones de llenado según días.  
- **Boxplot por hora del día** → valores atípicos y tendencias horarias.  

---

## 📖 Storytelling y Análisis Visual
1. **Contenedores críticos** → Se observó que los contenedores dañados presentan valores extremos en porcentaje de llenado.  
2. **Rutas eficientes vs. ineficientes** → Al comparar tiempos de duración y cantidad de contenedores, se identifican rutas más óptimas.  
3. **Patrones semanales** → Los sensores muestran mayor porcentaje de llenado a inicios de semana (lunes y martes), lo que sugiere ajustar la planeación.  
4. **Anomalías detectadas** → Boxplots de sensores ayudan a identificar lecturas fuera de rango (ej. > 100%), que corresponden a fallas o datos atípicos.  

---

## 🚀 Ejecución del Dashboard
Para iniciar el dashboard localmente:
```bash
streamlit run dashboard/dashboard.py
```
Esto abrirá automáticamente en el navegador:
👉 http://localhost:8501
 ---
 ## pruevas de regresion
Para iniciar pruebas en los endpoints principales ejecute:
```bash
python -m pytest -v --import-mode=importlib
```


**Proyecto:** SmartWasteApi

