"""
import requests
from app.tests.test_auth import test_login_usuario
from datetime import datetime

BASE_URL = "http://127.0.0.1:8000/api/sensores"

def test_crear_sensor():
    token = test_login_usuario()
    headers = {"Authorization": f"Bearer {token}"}
    data = {
        "Tipo": "Ultrasonido",
        "Descripcion": "Sensor de llenado principal",
        "Estatus": True,
        "Fecha_Registro": datetime.now().isoformat(),
        "Contenedor_Id": 5
    }
    response = requests.post(f"{BASE_URL}/sensor/", json=data, headers=headers)
    assert response.status_code in (200, 201)
    print("✅ Sensor creado correctamente")

def test_listar_sensores():
    token = test_login_usuario()
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{BASE_URL}/sensor/", headers=headers)
    assert response.status_code == 200
    print("✅ Sensores listados correctamente")
"""
