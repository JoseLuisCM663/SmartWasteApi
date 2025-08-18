import pandas as pd
import numpy as np
import os
import joblib
from sqlalchemy.orm import Session
from app.models.bitacora_recolecion import BitacoraRecoleccion
from app.models.bitacora_contenedor import BitacoraContenedor
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, f1_score, classification_report

# Carpeta para guardar modelo
MODEL_PATH = "datos/modelos/modelo_rutas.pkl"

def entrenar_modelo_bitacoras(ruta_recoleccion_csv: str, ruta_contenedor_csv: str):
    """
    Entrena un modelo supervisado para clasificar rutas en 'Eficiente' o 'Ineficiente'.
    Usa datos de bitácora de recolección y contenedores.
    """

    try:
        # Leer datasets
        df_recoleccion = pd.read_csv(ruta_recoleccion_csv)
        df_contenedor = pd.read_csv(ruta_contenedor_csv)

        # --- PREPROCESAMIENTO ---
        # Convertir fechas
        df_recoleccion["Fecha_Registro"] = pd.to_datetime(df_recoleccion["Fecha_Registro"], errors="coerce")
        df_contenedor["Fecha_Registro"] = pd.to_datetime(df_contenedor["Fecha_Registro"], errors="coerce")

        # Métricas agregadas por ruta
        df_contenedor_grouped = df_contenedor.groupby("Bitacora_Id").agg({
            "Porcentaje_Llenado": "mean",
            "Recolectado": "mean"
        }).reset_index()

        df = df_recoleccion.merge(df_contenedor_grouped, left_on="ID", right_on="Bitacora_Id", how="left")

        # Definir etiqueta (target): Eficiente vs Ineficiente
        def clasificar(row):
            if row["Tiempo_Duracion"] <= 100 and row["Recolectado"] >= 0.8:
                return 1  # Eficiente
            return 0  # Ineficiente

        df["Etiqueta"] = df.apply(clasificar, axis=1)

        # Features
        X = df[["Tiempo_Duracion", "Cantidad_Contenedores", "Porcentaje_Llenado", "Recolectado"]].fillna(0)
        y = df["Etiqueta"]

        # Split train/test
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

        # Modelo
        modelo = RandomForestClassifier(n_estimators=100, random_state=42)
        modelo.fit(X_train, y_train)

        # Evaluación
        y_pred = modelo.predict(X_test)
        acc = accuracy_score(y_test, y_pred)
        f1 = f1_score(y_test, y_pred)

        # Guardar modelo
        os.makedirs(os.path.dirname(MODEL_PATH), exist_ok=True)
        joblib.dump(modelo, MODEL_PATH)

        return {
            "mensaje": "Modelo entrenado y guardado",
            "accuracy": round(acc, 2),
            "f1_score": round(f1, 2),
            "reporte": classification_report(y_test, y_pred, target_names=["Ineficiente", "Eficiente"])
        }

    except Exception as e:
        return {"error": f"Error entrenando modelo: {e}"}

def predecir_ruta_por_bitacora(bitacora_id: int, db: Session):
    """
    Predice si una ruta de recolección (bitácora) fue eficiente o ineficiente.
    Obtiene datos de las tablas BitacoraRecoleccion y BitacoraContenedor.
    """

    try:
        if not os.path.exists(MODEL_PATH):
            return {"error": "Modelo no entrenado. Entrena primero."}

        # --- 1) Obtener bitácora de recolección ---
        reco = db.query(BitacoraRecoleccion).filter(BitacoraRecoleccion.ID == bitacora_id).first()
        if not reco:
            return {"error": f"No se encontró BitacoraRecoleccion con ID {bitacora_id}"}

        # --- 2) Obtener contenedores asociados ---
        contenedores = db.query(BitacoraContenedor).filter(BitacoraContenedor.Bitacora_Id == bitacora_id).all()

        if not contenedores:
            return {"error": f"No hay contenedores asociados a Bitacora {bitacora_id}"}

        # Calcular métricas agregadas
        promedio_lleno = sum([c.Porcentaje_Llenado or 0 for c in contenedores]) / len(contenedores)
        promedio_recolectado = sum([1 if c.Recolectado else 0 for c in contenedores]) / len(contenedores)

        features = {
            "Tiempo_Duracion": reco.Tiempo_Duracion or 0,
            "Cantidad_Contenedores": reco.Cantidad_Contenedores or len(contenedores),
            "Porcentaje_Llenado": promedio_lleno,
            "Recolectado": promedio_recolectado
        }

        # --- 3) Cargar modelo y predecir ---
        modelo = joblib.load(MODEL_PATH)
        X_new = pd.DataFrame([features])
        pred = modelo.predict(X_new)[0]

        return {
            "bitacora_id": bitacora_id,
            "prediccion": "Eficiente" if pred == 1 else "Ineficiente",
            "features": features
        }

    except Exception as e:
        return {"error": f"Error en predicción: {e}"}
