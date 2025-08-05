from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.responses import FileResponse
from app.database import get_db
from app.utils.etl_export import exportar_lecturas_sensor
import os

router_exportar = APIRouter()

@router_exportar.get("/exportar-csv/")
def descargar_csv(sensor_id: int, db: Session = Depends(get_db)):
    """
    Exporta lecturas de un sensor a CSV limpio y lo devuelve como descarga.
    """
    try:
        output_folder = "datos"
        os.makedirs(output_folder, exist_ok=True)

        ruta_csv = f"{output_folder}/lecturas_sensor_{sensor_id}.csv"
        exportar_lecturas_sensor(sensor_id, ruta_csv, db)

        return FileResponse(
            ruta_csv,
            media_type='text/csv',
            filename=f"lecturas_sensor_{sensor_id}.csv"
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
