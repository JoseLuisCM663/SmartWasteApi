import os
from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
from app.crud import ml_unsupervised

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))  # SmartWasteApi/
DATA_DIR = os.path.join(BASE_DIR, "datos")
MODELOS_DIR = os.path.join(DATA_DIR, "modelos")
os.makedirs(MODELOS_DIR, exist_ok=True)

router_ml = APIRouter(prefix="/ml_unsupervised", tags=["ML No Supervisado"])

@router_ml.get("/entrenar/")
def entrenar_modelo(n_clusters: int = 3):
    try:
        csv_path = os.path.join(DATA_DIR, "lecturas_todos_sensores.csv")
        print(f"🔍 Cargando CSV desde: {csv_path}")
        if not os.path.exists(csv_path):
            raise HTTPException(status_code=404, detail="CSV no encontrado")

        df = ml_unsupervised.entrenar_clustering(csv_path, n_clusters)

        informe_path = os.path.join(DATA_DIR, "informe_clusters.pdf")
        ml_unsupervised.generar_informe_pdf(df, informe_path)

        return {
            "detail": "Modelo entrenado y PDF generado",
            "modelo_path": os.path.join(MODELOS_DIR, "kmeans_model.pkl"),
            "informe_path": informe_path
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router_ml.get("/descargar-informe/")
def descargar_informe():
    informe_path = os.path.join(DATA_DIR, "informe_clusters.pdf")
    if not os.path.exists(informe_path):
        raise HTTPException(status_code=404, detail="Informe PDF no encontrado")
    return FileResponse(
        informe_path,
        media_type="application/pdf",
        filename="informe_clusters.pdf"
    )
