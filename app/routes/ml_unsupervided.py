import os
from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
from app.crud import ml_unsupervised

router_ml = APIRouter(prefix="/ml_unsupervised", tags=["ML No Supervisado"])

@router_ml.get("/entrenar/")
def entrenar_modelo(n_clusters: int = 3):
    """
    Entrena el modelo K-Means usando CSV de todas las lecturas,
    guarda el modelo en datos/modelos y genera un informe PDF.
    """
    try:
        csv_path = "datos/lecturas_todos_sensores.csv"
        if not os.path.exists(csv_path):
            raise HTTPException(status_code=404, detail="CSV no encontrado")

        # Entrenar modelo y agregar clusters
        df = ml_unsupervised.entrenar_clustering(csv_path, n_clusters)

        # Generar informe PDF
        informe_path = "datos/informe_clusters.pdf"
        ml_unsupervised.generar_informe_pdf(df, informe_path)

        return {
            "detail": "Modelo entrenado y PDF generado",
            "modelo_path": "datos/modelos/kmeans_model.pkl",
            "informe_path": informe_path
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router_ml.get("/descargar-informe/")
def descargar_informe():
    """
    Descarga el PDF generado del clustering.
    """
    informe_path = "datos/informe_clusters.pdf"
    if not os.path.exists(informe_path):
        raise HTTPException(status_code=404, detail="Informe PDF no encontrado")
    return FileResponse(
        informe_path,
        media_type="application/pdf",
        filename="informe_clusters.pdf"
    )
