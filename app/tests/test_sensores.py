import requests
from app.tests.test_auth import obtener_token
from datetime import datetime

BASE_URL = "http://127.0.0.1:8000/api/sensores"
SENSOR_ID_CREADO = None  # Variable global para almacenar el ID del sensor recién creado


def test_crear_sensor():
    """📡 Verifica que se puede crear un sensor correctamente."""
    global SENSOR_ID_CREADO

    token = obtener_token()
    headers = {"Authorization": f"Bearer {token}"}

    data = {
        "Tipo": "Ultrasonido",
        "Descripcion": f"Sensor de llenado {int(datetime.now().timestamp())}",
        "Estatus": True,
        "Fecha_Registro": datetime.now().isoformat(),
        "Contenedor_ID": 1  # ⚠️ Asegúrate de que este contenedor exista en la base de datos
    }

    response = requests.post(f"{BASE_URL}/sensor", json=data, headers=headers)
    assert response.status_code in (200, 201), f"❌ Error al crear sensor: {response.text}"

    sensor = response.json()
    assert "ID" in sensor, "❌ El sensor creado no tiene un ID asignado"
    SENSOR_ID_CREADO = sensor["ID"]
    print(f"✅ Sensor creado correctamente con ID {SENSOR_ID_CREADO}")


def test_obtener_sensor_por_id():
    """🔍 Verifica que se puede obtener el sensor recién creado por su ID."""
    global SENSOR_ID_CREADO
    assert SENSOR_ID_CREADO is not None, "❌ No se ha creado un sensor previamente"

    token = obtener_token()
    headers = {"Authorization": f"Bearer {token}"}

    response = requests.get(f"{BASE_URL}/sensor/{SENSOR_ID_CREADO}", headers=headers)
    assert response.status_code == 200, f"❌ Error al obtener sensor: {response.text}"

    sensor = response.json()
    assert sensor["ID"] == SENSOR_ID_CREADO, "❌ El ID del sensor obtenido no coincide"
    print(f"🔍 Sensor obtenido correctamente: {sensor['Descripcion']}")

def test_listar_sensores():
    """📋 Verifica que el listado de sensores funcione correctamente."""
    token = obtener_token()
    headers = {"Authorization": f"Bearer {token}"}

    response = requests.get(f"{BASE_URL}/sensor", headers=headers)
    assert response.status_code == 200, f"❌ Error al listar sensores: {response.text}"

    sensores = response.json()
    assert isinstance(sensores, list), "❌ La respuesta no es una lista"
    print(f"✅ {len(sensores)} sensores listados correctamente")

def test_actualizar_sensor():
    """✏️ Verifica que se puede actualizar un sensor existente."""
    global SENSOR_ID_CREADO
    assert SENSOR_ID_CREADO is not None, "❌ No se ha creado un sensor previamente"

    token = obtener_token()
    headers = {"Authorization": f"Bearer {token}"}

    data = {
        "Tipo": "Ultrasonido",  # obligatorio según tu modelo
        "Descripcion": f"Sensor actualizado {int(datetime.now().timestamp())}",
        "Estatus": False,
        "Fecha_Actualizacion": datetime.now().isoformat()
    }

    response = requests.put(
        f"{BASE_URL}/sensor/{SENSOR_ID_CREADO}",
        json=data,
        headers=headers
    )
    assert response.status_code in (200, 204), f"❌ Error al actualizar sensor: {response.text}"
    print(f"✏️ Sensor con ID {SENSOR_ID_CREADO} actualizado correctamente")

def test_eliminar_sensor():
    """🗑️ Verifica que se puede eliminar el sensor recién creado."""
    global SENSOR_ID_CREADO
    assert SENSOR_ID_CREADO is not None, "❌ No se ha creado un sensor previamente"

    token = obtener_token()
    headers = {"Authorization": f"Bearer {token}"}

    response = requests.delete(f"{BASE_URL}/sensor/{SENSOR_ID_CREADO}", headers=headers)
    assert response.status_code in (200, 204), f"❌ Error al eliminar sensor: {response.text}"
    print(f"🗑️ Sensor con ID {SENSOR_ID_CREADO} eliminado correctamente")

    # Confirmar eliminación
    verificar = requests.get(f"{BASE_URL}/sensor/{SENSOR_ID_CREADO}", headers=headers)
    assert verificar.status_code == 404, f"❌ El sensor aún existe tras eliminarlo: {verificar.text}"
    print("✅ Verificación completa: el sensor fue eliminado correctamente.")
