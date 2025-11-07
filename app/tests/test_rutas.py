import requests
from app.tests.test_auth import obtener_token
from datetime import datetime

BASE_URL = "http://127.0.0.1:8000/api/rutas_recoleccion"
RUTA_ID_CREADA = None


def test_crear_ruta():
    """🚚 Verifica que se puede crear una ruta de recolección correctamente."""
    global RUTA_ID_CREADA

    token = obtener_token()
    headers = {"Authorization": f"Bearer {token}"}

    data = {
        "Nombre": f"Ruta de prueba {int(datetime.now().timestamp())}",
        "Descripcion": "Zona norte",
        "Fecha_Registro": datetime.now().isoformat(),
        "Estatus": True
    }

    response = requests.post(f"{BASE_URL}/ruta_recoleccion/", json=data, headers=headers)
    assert response.status_code in (200, 201), f"❌ Error al crear ruta: {response.text}"

    ruta = response.json()
    assert "ID" in ruta, "❌ La ruta creada no tiene un ID asignado"

    RUTA_ID_CREADA = ruta["ID"]
    print(f"✅ Ruta creada correctamente con ID {RUTA_ID_CREADA}")


def test_listar_rutas():
    """📋 Verifica que el listado de rutas funciona correctamente."""
    token = obtener_token()
    headers = {"Authorization": f"Bearer {token}"}

    response = requests.get(f"{BASE_URL}/ruta_recoleccion/", headers=headers)
    assert response.status_code == 200, f"❌ Error al listar rutas: {response.text}"

    rutas = response.json()
    assert isinstance(rutas, list), "❌ La respuesta no es una lista"
    print(f"✅ {len(rutas)} rutas listadas correctamente")


def test_obtener_ruta_por_id():
    """🔍 Verifica que se puede obtener la ruta recién creada."""
    global RUTA_ID_CREADA
    assert RUTA_ID_CREADA is not None, "❌ No se ha creado una ruta previamente"

    token = obtener_token()
    headers = {"Authorization": f"Bearer {token}"}

    response = requests.get(f"{BASE_URL}/ruta_recoleccion/{RUTA_ID_CREADA}", headers=headers)
    assert response.status_code == 200, f"❌ Error al obtener ruta: {response.text}"

    ruta = response.json()
    assert ruta["ID"] == RUTA_ID_CREADA, "❌ El ID de la ruta no coincide"
    print(f"🔍 Ruta obtenida correctamente: {ruta['Nombre']}")


def test_actualizar_ruta():
    """✏️ Verifica que se puede actualizar una ruta existente."""
    global RUTA_ID_CREADA
    assert RUTA_ID_CREADA is not None, "❌ No se ha creado una ruta previamente"

    token = obtener_token()
    headers = {"Authorization": f"Bearer {token}"}

    datos_actualizados = {
        "Nombre": f"Ruta actualizada {int(datetime.now().timestamp())}",
        "Descripcion": "Zona sur actualizada",
        "Estatus": False,
        "Fecha_Actualizacion": datetime.now().isoformat()
    }

    response = requests.put(f"{BASE_URL}/ruta_recoleccion/{RUTA_ID_CREADA}", json=datos_actualizados, headers=headers)
    assert response.status_code == 200, f"❌ Error al actualizar ruta: {response.text}"

    ruta = response.json()
    assert ruta["Nombre"] == datos_actualizados["Nombre"], "❌ La ruta no se actualizó correctamente"
    print(f"✏️ Ruta actualizada correctamente: {ruta['Nombre']}")

def test_eliminar_ruta():
    """🗑️ Verifica que se puede eliminar la ruta recién creada."""
    global RUTA_ID_CREADA
    assert RUTA_ID_CREADA is not None, "❌ No se ha creado una ruta previamente"

    token = obtener_token()
    headers = {"Authorization": f"Bearer {token}"}

    response = requests.delete(f"{BASE_URL}/ruta_recoleccion/{RUTA_ID_CREADA}", headers=headers)
    assert response.status_code in (200, 204), f"❌ Error al eliminar ruta: {response.text}"

    print(f"🗑️ Ruta con ID {RUTA_ID_CREADA} eliminada correctamente")

    # Verificar que la ruta ya no exista
    verificar = requests.get(f"{BASE_URL}/ruta_recoleccion/{RUTA_ID_CREADA}", headers=headers)
    assert verificar.status_code == 404, f"❌ La ruta aún existe después de eliminarla: {verificar.text}"
    print("✅ Verificación completa: la ruta fue eliminada correctamente.")
