# app/tests/test_usuarios.py
import requests
from app.tests.test_auth import obtener_token  # Importamos la función auxiliar
from datetime import datetime

BASE_URL = "http://127.0.0.1:8000/api/usuarios"

def test_listar_usuarios():
    """Prueba autenticada: lista los usuarios utilizando el token obtenido desde test_auth.py."""
    token = obtener_token()
    headers = {"Authorization": f"Bearer {token}"}

    response = requests.get(f"{BASE_URL}/usuario", headers=headers)
    assert response.status_code == 200, f"Error al listar usuarios: {response.text}"
    assert isinstance(response.json(), list), "La respuesta no es una lista de usuarios"

    print("✅ Usuarios listados correctamente")

def test_crear_usuario():
    """🧩 Verifica que se puede crear un nuevo usuario con los campos correctos."""
    token = obtener_token()
    headers = {"Authorization": f"Bearer {token}"}

    nuevo_usuario = {
        "Nombre_Usuario": f"user_{int(datetime.now().timestamp())}",
        "Tipo_Usuario": "Administrador",
        "Correo_Electronico": f"user{int(datetime.now().timestamp())}@example.com",
        "Contrasena": "admin1234",
        "Numero_Telefonico_Movil": "7711234567",
        "Estatus": True,
        "Fecha_Registro": datetime.now().isoformat(),
        "Fecha_Actualizacion": datetime.now().isoformat()
    }

    response = requests.post(f"{BASE_URL}/registro", json=nuevo_usuario, headers=headers)
    assert response.status_code in (200, 201), f"Error al crear usuario: {response.text}"
    print("✅ Usuario creado  correctamente")

def test_obtener_usuario_por_id():
    """🔎 Verifica que se puede obtener un usuario existente (por ID válido)."""
    token = obtener_token()
    headers = {"Authorization": f"Bearer {token}"}

    usuario_id = 1  # Asegúrate que este ID exista en tu base de datos
    response = requests.get(f"{BASE_URL}/usuario/{usuario_id}", headers=headers)
    assert response.status_code == 200, f"Error al obtener usuario: {response.text}"
    assert "Correo_Electronico" in response.json(), "No se encontró el campo esperado"
    print("✅ Usuario obtenido correctamente")

def test_actualizar_usuario():
    """✏️ Verifica que se puede actualizar un usuario existente."""
    token = obtener_token()
    headers = {"Authorization": f"Bearer {token}"}

    usuario_id = 4  # ID existente
    datos_actualizados = {
        "Nombre_Usuario": f"user_actualizado_{int(datetime.now().timestamp())}",
        "Tipo_Usuario": "Administrador",
        "Correo_Electronico": f"user_update{int(datetime.now().timestamp())}@example.com",
        "Contrasena": "admin123",
        "Numero_Telefonico_Movil": "7719876543",
        "Estatus": True,
        "Fecha_Actualizacion": datetime.now().isoformat(),
        "Fecha_Registro": datetime.now().isoformat()
    }

    response = requests.put(
        f"{BASE_URL}/usuario/{usuario_id}", 
        json=datos_actualizados, 
        headers=headers
    )

    assert response.status_code == 200, f"Error al actualizar usuario: {response.text}"
    print("✅ Usuario actualizado correctamente")

def test_eliminar_usuario():
    """🗑️ Crea y luego elimina un usuario temporal."""
    token = obtener_token()
    headers = {"Authorization": f"Bearer {token}"}

    # Crear usuario temporal
    temp_user = {
        "Nombre_Usuario": f"user_delete_{int(datetime.now().timestamp())}",
        "Tipo_Usuario": "Usuario",
        "Correo_Electronico": f"delete{int(datetime.now().timestamp())}@example.com",
        "Contrasena": "admin123",
        "Numero_Telefonico_Movil": "7719876543",
        "Estatus": True,
        "Fecha_Registro": datetime.now().isoformat(),
        "Fecha_Actualizacion": datetime.now().isoformat()
    }

    creado = requests.post(f"{BASE_URL}/registro", json=temp_user, headers=headers)
    assert creado.status_code in (200, 201), f"Error al crear usuario temporal: {creado.text}"

    usuario_id = creado.json().get("ID")
    assert usuario_id, "No se obtuvo el ID del usuario creado"

    # Eliminarlo
    eliminado = requests.delete(f"{BASE_URL}/usuario/{usuario_id}", headers=headers)
    assert eliminado.status_code in (200, 204), f"Error al eliminar usuario: {eliminado.text}"
    print("✅ Usuario eliminado correctamente")