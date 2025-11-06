# app/tests/test_auth.py
import requests

BASE_URL = "http://127.0.0.1:8000/api"
LOGIN_URL = f"{BASE_URL}/usuarios/login"

def obtener_token():
    """
    Función auxiliar para autenticación.
    No se ejecuta como test; solo devuelve un token válido.
    """
    data = {
        "Correo_Electronico": "donaldgarcia@example.net",
        "Contrasena": "admin123"
    }

    response = requests.post(LOGIN_URL, json=data)
    assert response.status_code == 200, f"Error al iniciar sesión: {response.text}"

    token = response.json().get("access_token")
    assert token is not None, "No se recibió token en la respuesta"
    print("✅ Token obtenido correctamente")
    return token

def test_login_usuario():
    """Prueba simple que valida el login sin retornar el token."""
    token = obtener_token()
    assert isinstance(token, str)
