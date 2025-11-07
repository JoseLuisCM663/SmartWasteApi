# app/tests/test_auth.py
import requests

BASE_URL = "http://127.0.0.1:8000/api"
USUARIOS_URL = f"{BASE_URL}/usuarios"
LOGIN_URL = f"{USUARIOS_URL}/login"


def obtener_token():
    """
    Función auxiliar para autenticación.
    Si el usuario no existe, lo crea antes de hacer login.
    Devuelve un token JWT válido.
    """
    # Datos del usuario de prueba
    user_data = {
        "Nombre_Usuario": "usuario_test",
        "Correo_Electronico": "donaldgarcia@example.net",
        "Contrasena": "admin123",
        "Numero_Telefonico_Movil": "1234567890",
        "Estatus": True
    }

    # Intentar crear el usuario (si ya existe, la API devolverá 400 o 409)
    crear_resp = requests.post(f"{USUARIOS_URL}/", json=user_data)
    if crear_resp.status_code in (200, 201):
        print("👤 Usuario de prueba creado correctamente")
    else:
        print(f"ℹ️ Usuario posiblemente ya existente: {crear_resp.text}")

    # Intentar iniciar sesión
    login_data = {
        "Correo_Electronico": user_data["Correo_Electronico"],
        "Contrasena": user_data["Contrasena"]
    }
    response = requests.post(LOGIN_URL, json=login_data)

    # Validar login exitoso
    assert response.status_code == 200, f"❌ Error al iniciar sesión: {response.text}"

    token = response.json().get("access_token")
    assert token is not None, "❌ No se recibió token en la respuesta"
    print("✅ Token obtenido correctamente")
    return token


def test_login_usuario():
    """Prueba simple que valida el login sin retornar el token."""
    token = obtener_token()
    assert isinstance(token, str)
    print("🧪 Prueba de login ejecutada correctamente")
