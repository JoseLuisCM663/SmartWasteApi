import requests
from app.tests.test_auth import obtener_token
from datetime import datetime

BASE_URL = "http://127.0.0.1:8000/api/contenedores"
CONTENEDOR_ID_CREADO = None


def test_crear_contenedor():
    """🧱 Verifica que se puede crear un contenedor correctamente."""
    global CONTENEDOR_ID_CREADO

    token = obtener_token()
    headers = {"Authorization": f"Bearer {token}"}

    data = {
        "Ubicacion": f"Calle Hidalgo {int(datetime.now().timestamp())}",
        "Capacidad": 120,
        "Ruta_ID": 1,  # ⚠️ Asegúrate de que esta ruta exista
        "Descripcion": "Contenedor orgánico",
        "Estatus": True,
        "Fecha_Registro": datetime.now().isoformat()
    }

    response = requests.post(f"{BASE_URL}/contenedor", json=data, headers=headers)
    assert response.status_code in (200, 201), f"❌ Error al crear contenedor: {response.text}"

    contenedor = response.json()
    assert "ID" in contenedor, "❌ El contenedor creado no tiene un ID asignado"

    CONTENEDOR_ID_CREADO = contenedor["ID"]
    print(f"✅ Contenedor creado correctamente con ID {CONTENEDOR_ID_CREADO}")


def test_obtener_contenedor_por_id():
    """🔍 Verifica que se puede obtener el contenedor recién creado."""
    global CONTENEDOR_ID_CREADO
    assert CONTENEDOR_ID_CREADO is not None, "❌ No se ha creado un contenedor previamente"

    token = obtener_token()
    headers = {"Authorization": f"Bearer {token}"}

    response = requests.get(f"{BASE_URL}/contenedor/{CONTENEDOR_ID_CREADO}", headers=headers)
    assert response.status_code == 200, f"❌ Error al obtener contenedor: {response.text}"

    contenedor = response.json()
    assert contenedor["ID"] == CONTENEDOR_ID_CREADO, "❌ El ID del contenedor no coincide"

    print(f"🔍 Contenedor obtenido correctamente: {contenedor['Descripcion']}")


def test_listar_contenedores():
    """📋 Verifica que el listado de contenedores funciona correctamente."""
    token = obtener_token()
    headers = {"Authorization": f"Bearer {token}"}
    
    response = requests.get(f"{BASE_URL}/contenedor", headers=headers)
    assert response.status_code == 200, f"Error al listar contenedores: {response.text}"
    
    contenedores = response.json()
    assert isinstance(contenedores, list), "La respuesta no es una lista"
    print(f"✅ {len(contenedores)} contenedores listados correctamente")


def test_actualizar_contenedor():
    """✏️ Verifica que se puede actualizar el contenedor recién creado."""
    global CONTENEDOR_ID_CREADO
    assert CONTENEDOR_ID_CREADO is not None, "❌ No se ha creado un contenedor previamente"

    token = obtener_token()
    headers = {"Authorization": f"Bearer {token}"}

    datos_actualizados = {
        "Ubicacion": "Calle Morelos Actualizada",
        "Capacidad": 200,
        "Descripcion": "Contenedor actualizado",
        "Estatus": False,
        "Fecha_Actualizacion": datetime.now().isoformat()
    }

    response = requests.put(f"{BASE_URL}/contenedor/{CONTENEDOR_ID_CREADO}", json=datos_actualizados, headers=headers)
    assert response.status_code == 200, f"❌ Error al actualizar contenedor: {response.text}"

    contenedor = response.json()
    assert contenedor["Ubicacion"] == datos_actualizados["Ubicacion"], "❌ La ubicación no se actualizó correctamente"
    print(f"✏️ Contenedor actualizado correctamente: {contenedor['Descripcion']}")


def test_eliminar_contenedor():
    """🗑️ Verifica que se puede eliminar el contenedor recién creado."""
    global CONTENEDOR_ID_CREADO
    assert CONTENEDOR_ID_CREADO is not None, "❌ No se ha creado un contenedor previamente"

    token = obtener_token()
    headers = {"Authorization": f"Bearer {token}"}

    response = requests.delete(f"{BASE_URL}/contenedor/{CONTENEDOR_ID_CREADO}", headers=headers)
    assert response.status_code == 200, f"❌ Error al eliminar contenedor: {response.text}"

    print(f"🗑️ Contenedor con ID {CONTENEDOR_ID_CREADO} eliminado correctamente")

    # Verificar que ya no exista
    verificar = requests.get(f"{BASE_URL}/contenedor/{CONTENEDOR_ID_CREADO}", headers=headers)
    assert verificar.status_code == 404, f"❌ El contenedor aún existe después de eliminarlo: {verificar.text}"
    print("✅ Verificación completa: el contenedor fue eliminado correctamente.")
