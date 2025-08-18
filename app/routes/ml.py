from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.crud import ml_model

router_ml = APIRouter(
    prefix="/ml",
    tags=["Machine Learning"]
)


@router_ml.post("/entrenar/")
def entrenar_modelo():
    """
    Entrena el modelo de clasificación de rutas usando los CSV de bitácoras.
    """
    try:
        resultado = ml_model.entrenar_modelo_bitacoras(
            "datos/bitacora_recoleccion_etl.csv",
            "datos/bitacora_contenedor_etl.csv"
        )
        if "error" in resultado:
            raise Exception(resultado["error"])
        return resultado
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router_ml.get("/predecir/")
def predecir_ruta(bitacora_id: int, db: Session = Depends(get_db)):
    """
    Clasifica si una ruta de recolección (bitácora) es eficiente o ineficiente.
    Usa datos de BitacoraRecoleccion y BitacoraContenedor.
    """
    try:
        resultado = ml_model.predecir_ruta_por_bitacora(bitacora_id, db)

        if "error" in resultado:
            raise HTTPException(status_code=404, detail=resultado["error"])

        return resultado

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error en predicción: {e}")