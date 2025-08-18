from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.responses import FileResponse
from app.database import get_db
from app.utils.etl_export import exportar_todas_lecturas, etl_bitacoras
import os
import zipfile

router_exportar = APIRouter()

@router_exportar.get("/exportar-todos/")
def descargar_csv_todos(db: Session = Depends(get_db)):
    """
    Exporta lecturas de TODOS los sensores a un CSV limpio y lo devuelve como descarga.
    Cumple con el ETL: extracción, transformación, limpieza, manejo de outliers y carga.
    """
    try:
        output_folder = "datos"
        os.makedirs(output_folder, exist_ok=True)

        ruta_csv = f"{output_folder}/lecturas_todos_sensores.csv"
        exportar_todas_lecturas(ruta_csv, db)

        return FileResponse(
            ruta_csv,
            media_type="text/csv",
            filename="lecturas_todos_sensores.csv"
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router_exportar.get("/exportar-bitacoras/")
def descargar_bitacoras_etl(db: Session = Depends(get_db)):
    """
    Ejecuta limpieza y exportación ETL de bitácoras, y devuelve archivos CSV en un ZIP.
    """
    try:
        output_folder = "datos"
        os.makedirs(output_folder, exist_ok=True)

        # Ejecuta ETL
        df_recoleccion, df_contenedor = etl_bitacoras(db)

        if df_recoleccion is None or df_contenedor is None:
            raise Exception("No se pudo generar ETL correctamente.")

        # Exportar CSVs
        ruta_rec = os.path.join(output_folder, "bitacora_recoleccion_etl.csv")
        ruta_cont = os.path.join(output_folder, "bitacora_contenedor_etl.csv")

        df_recoleccion.to_csv(ruta_rec, index=False)
        df_contenedor.to_csv(ruta_cont, index=False)

        # Crear un ZIP con ambos
        zip_path = os.path.join(output_folder, "bitacoras_etl.zip")
        with zipfile.ZipFile(zip_path, "w") as zipf:
            zipf.write(ruta_rec, arcname="bitacora_recoleccion_etl.csv")
            zipf.write(ruta_cont, arcname="bitacora_contenedor_etl.csv")

        return FileResponse(
            zip_path,
            media_type='application/zip',
            filename="bitacoras_etl.zip"
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al generar ETL: {e}")