import requests
from app.tests.test_auth import test_login_usuario
from datetime import datetime

BASE_URL = "http://127.0.0.1:8000/api/contenedores"

def test_crear_contenedor():
    token = test_login_usuario()
    headers = {"Authorization": f"Bearer {token}"}
    data = {
        "Ubicacion": "Calle Hidalgo 32",
        "Capacidad": 120,
        "Ruta_Id": 1,
        "Descripcion": "Contenedor orgánico",
        "Estatus": True,
        "Fecha_Registro": datetime.now().isoformat()
    }
    response = requests.post(f"{BASE_URL}/contenedor/", json=data, headers=headers)
    assert response.status_code in (200, 201)
    print("✅ Contenedor creado correctamente")

def test_listar_contenedores():
    token = test_login_usuario()
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{BASE_URL}/contenedor/", headers=headers)
    assert response.status_code == 200
    print("✅ Contenedores listados correctamente")
