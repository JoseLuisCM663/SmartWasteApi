import requests
from app.tests.test_auth import test_login_usuario

BASE_URL = "http://127.0.0.1:8000/api/usuarios"

def test_listar_usuarios():
    token = test_login_usuario()
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{BASE_URL}/usuarios/", headers=headers)
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    print("✅ Usuarios listados correctamente")
