import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

@pytest.fixture
def producto_data():
    return {"nombre": "Test Producto", "precio": 10.5, "tamano": 2.0}


def test_create_producto(producto_data):
    response = client.post("/productos/", json=producto_data)
    assert response.status_code == 201 or response.status_code == 200
    data = response.json()
    assert data["nombre"] == producto_data["nombre"]
    assert data["precio"] == producto_data["precio"]
    assert data["tamano"] == producto_data["tamano"]


def test_get_productos():
    response = client.get("/productos/")
    assert response.status_code == 200
    assert isinstance(response.json(), list) or "data" in response.json()


def test_update_producto(producto_data):
    # Crear producto
    create_resp = client.post("/productos/", json=producto_data)
    producto_id = create_resp.json()["id"]
    # Actualizar producto
    update_data = {"nombre": "Producto Actualizado"}
    update_resp = client.put(f"/productos/{producto_id}", json=update_data)
    assert update_resp.status_code == 200
    assert update_resp.json()["nombre"] == "Producto Actualizado"


def test_delete_producto(producto_data):
    # Crear producto
    create_resp = client.post("/productos/", json=producto_data)
    producto_id = create_resp.json()["id"]
    # Eliminar producto
    delete_resp = client.delete(f"/productos/{producto_id}")
    assert delete_resp.status_code == 200 or delete_resp.status_code == 204
