# app/routes/dw_routes.py
from fastapi import APIRouter, HTTPException
from app.utils.dw_etl import (
    cargar_dim_sensor,
    cargar_dim_contenedor,
    cargar_dim_ruta,
    cargar_fact_lecturas,
    cargar_dim_usuario,
    cargar_dim_tiempo
)


router_dw = APIRouter(prefix="/dw", tags=["Data Warehouse"])

@router_dw.post("/actualizar/")
def actualizar_dw():
    """
    Ejecuta el proceso ETL para actualizar el Data Warehouse.
    """
    try:
        print("🔄 Iniciando ETL para Data Warehouse...")
        cargar_dim_usuario()
        cargar_dim_ruta()
        cargar_dim_contenedor()
        cargar_dim_sensor()
        cargar_dim_tiempo()
        cargar_fact_lecturas()
        print("✅ ETL completo. Data Warehouse actualizado.")
        return {"detail": "ETL completado exitosamente"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error en ETL: {str(e)}")
