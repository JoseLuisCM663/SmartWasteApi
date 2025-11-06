"""
import requests
from app.tests.test_auth import test_login_usuario
from datetime import datetime

BASE_URL = "http://127.0.0.1:8000/api/rutas_recolecion"

def test_crear_ruta():
    token = test_login_usuario()
    headers = {"Authorization": f"Bearer {token}"}
    data = {
        "Nombre": "Ruta de prueba",
        "Descripcion": "Zona norte",
        "Fecha_Registro": datetime.now().isoformat(),
        "Estatus": True
    }
    response = requests.post(f"{BASE_URL}/ruta_recolecion/", json=data, headers=headers)
    assert response.status_code in (200, 201)
    print("✅ Ruta creada correctamente")

def test_listar_rutas():
    token = test_login_usuario()
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{BASE_URL}/ruta_recolecion/", headers=headers)
    assert response.status_code == 200
    print("✅ Rutas listadas correctamente")
"""
