import streamlit as st
import pandas as pd
import plotly.express as px
import os

# Rutas de los CSV exportados por tu ETL
DATA_FOLDER = "public"
RECOLECCION_CSV = os.path.join(DATA_FOLDER, "bitacora_recoleccion_etl.csv")
CONTENEDOR_CSV = os.path.join(DATA_FOLDER, "bitacora_contenedor_etl.csv")

# --- Cargar datos ---
@st.cache_data
def cargar_datos():
    df_recoleccion = pd.read_csv(RECOLECCION_CSV) if os.path.exists(RECOLECCION_CSV) else pd.DataFrame()
    df_contenedor = pd.read_csv(CONTENEDOR_CSV) if os.path.exists(CONTENEDOR_CSV) else pd.DataFrame()
    return df_recoleccion, df_contenedor

df_recoleccion, df_contenedor = cargar_datos()

# --- Layout ---
st.set_page_config(page_title="SmartWaste Dashboard", layout="wide")
st.title("📊 SmartWaste - Dashboard Operativo")

# --- KPIs ---
st.subheader("🔹 Indicadores Clave")
col1, col2, col3 = st.columns(3)

if not df_recoleccion.empty:
    total_rutas = len(df_recoleccion)
    tiempo_prom = df_recoleccion["Tiempo_Duracion"].mean().round(1)
    total_contenedores = df_recoleccion["Cantidad_Contenedores"].sum()
else:
    total_rutas, tiempo_prom, total_contenedores = 0, 0, 0

col1.metric("🚛 Rutas registradas", total_rutas)
col2.metric("⏱️ Tiempo promedio (min)", tiempo_prom)
col3.metric("🗑️ Contenedores atendidos", total_contenedores)

# --- Gráfico de tiempos por ruta ---
st.subheader("📍 Tiempo de recolección por Ruta")
if not df_recoleccion.empty:
    fig = px.bar(df_recoleccion, x="Ruta_Id", y="Tiempo_Duracion", color="Cantidad_Contenedores",
                 title="Duración de rutas vs Contenedores")
    st.plotly_chart(fig, use_container_width=True)
else:
    st.warning("No hay datos de recolección cargados.")

# --- Estado de Contenedores ---
st.subheader("🗑️ Estado de Contenedores")
if not df_contenedor.empty:
    estado_counts = df_contenedor["Estado_Contenedor"].value_counts()
    fig2 = px.pie(values=estado_counts.values, names=estado_counts.index, title="Distribución de estados")
    st.plotly_chart(fig2, use_container_width=True)

    # Llenado de contenedores
    fig3 = px.histogram(df_contenedor, x="Porcentaje_Llenado", nbins=10, title="Distribución de llenado (%)")
    st.plotly_chart(fig3, use_container_width=True)
else:
    st.warning("No hay datos de contenedores cargados.")

# --- Tabla de bitácoras ---
st.subheader("📋 Bitácora de Recolecciones")
if not df_recoleccion.empty:
    st.dataframe(df_recoleccion)
else:
    st.info("Sin registros de bitácora.")

# --- Rutas adicionales ---
LECTURAS_SENSORES_CSV = os.path.join(DATA_FOLDER, "lecturas_todos_sensores.csv")

@st.cache_data
def cargar_datos():
    df_recoleccion = pd.read_csv(RECOLECCION_CSV) if os.path.exists(RECOLECCION_CSV) else pd.DataFrame()
    df_contenedor = pd.read_csv(CONTENEDOR_CSV) if os.path.exists(CONTENEDOR_CSV) else pd.DataFrame()
    df_sensores = pd.read_csv(LECTURAS_SENSORES_CSV) if os.path.exists(LECTURAS_SENSORES_CSV) else pd.DataFrame()
    return df_recoleccion, df_contenedor, df_sensores

df_recoleccion, df_contenedor, df_sensores = cargar_datos()

# --- Panel de Lecturas de Sensores ---
st.subheader("📡 Lecturas de Sensores en Tiempo")
if not df_sensores.empty:
    # Conversión de fecha
    df_sensores["Fecha"] = pd.to_datetime(df_sensores["Fecha"])

    # Selector de sensor
    sensores_disponibles = df_sensores["Sensor_Id"].unique().tolist()
    sensor_sel = st.selectbox("Selecciona un Sensor", sensores_disponibles)

    df_filtrado = df_sensores[df_sensores["Sensor_Id"] == sensor_sel]

    # Línea de valores por tiempo
    fig4 = px.line(df_filtrado, x="Fecha", y="Valor", title=f"Lecturas del Sensor {sensor_sel}", markers=True)
    st.plotly_chart(fig4, use_container_width=True)

    # Promedio de valores por día de la semana
    promedio_dia = df_filtrado.groupby("DiaSemana")["Valor"].mean().reset_index()
    fig5 = px.bar(promedio_dia, x="DiaSemana", y="Valor", title="Promedio por Día de la Semana", color="DiaSemana")
    st.plotly_chart(fig5, use_container_width=True)

    # Boxplot para detectar outliers
    fig6 = px.box(df_filtrado, x="Hora", y="Valor", points="all",
                  title=f"Distribución de valores por Hora - Sensor {sensor_sel}")
    st.plotly_chart(fig6, use_container_width=True)

    # Tabla cruda
    st.dataframe(df_filtrado)
else:
    st.warning("No hay lecturas de sensores cargadas.")
