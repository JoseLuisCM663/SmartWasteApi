import requests

BASE_URL = "http://127.0.0.1:8000/api"
LOGIN_URL = f"{BASE_URL}/usuarios/login"

def test_login_usuario():
    data = {
        "Correo_Electronico": "pepe@1",  # usa un usuario existente
        "Contrasena": "123456789"
    }
    response = requests.post(LOGIN_URL, json=data)
    assert response.status_code == 200, f"Error: {response.text}"
    token = response.json().get("access_token")
    assert token is not None
    print("✅ Token obtenido correctamente")
    return token
