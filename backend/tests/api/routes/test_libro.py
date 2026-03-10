import uuid

from fastapi.testclient import TestClient
from app.main import app

from app.core.config import settings
from tests.utils.libro import crear_libro_random

client = TestClient(app)

# Test para crear un libro vía endpoint
# Este test verifica que el endpoint /libros/ permite crear un libro correctamente.
def test_post_libro(
    client: TestClient, superuser_token_headers: dict[str, str]
) -> None:
    data = {
        "isbn": 1234567890123,
        "titulo": "El Quijote",
        "autor": "Cervantes",
        "editorial": "Espasa",
        "precio": 19.99
        }
    response = client.post(f"{settings.API_V1_STR}/libros/", 
    headers = superuser_token_headers,
    json=data
    )
    assert response.status_code == 201  # Verifica el código de respuesta
    data = response.json()
    assert data["titulo"] == "El Quijote"  # Verifica el título
    assert data["autor"] == "Cervantes"    # Verifica el autor

# Test para obtener un libro vía endpoint
# Este test verifica que el endpoint /libros/{id} permite recuperar un libro existente.
def test_get_libro():
    """
    Crea un libro y luego lo recupera por su ID usando el endpoint.
    """
    post_response = client.post("/libros/", json={
        "isbn": 1234567890123,
        "titulo": "El Quijote",
        "autor": "Cervantes",
        "editorial": "Espasa",
        "precio": 19.99
    })
    libro_id = post_response.json()["id"]
    get_response = client.get(f"/libros/{libro_id}")
    assert get_response.status_code == 200
    data = get_response.json()
    assert data["titulo"] == "El Quijote"

# Test para actualizar un libro vía endpoint
# Este test verifica que el endpoint PATCH /libros/{id} permite actualizar datos de un libro.
def test_patch_libro():
    """
    Crea un libro, lo actualiza y verifica que el cambio se refleje en la respuesta.
    """
    post_response = client.post("/libros/", json={
        "isbn": 1234567890123,
        "titulo": "El Quijote",
        "autor": "Cervantes",
        "editorial": "Espasa",
        "precio": 19.99
    })
    libro_id = post_response.json()["id"]
    patch_response = client.patch(f"/libros/{libro_id}", json={"precio": 25.00})
    assert patch_response.status_code == 200
    data = patch_response.json()
    assert data["precio"] == 25.00  # Verifica el nuevo precio

# Test para eliminar un libro vía endpoint
# Este test verifica que el endpoint DELETE /libros/{id} elimina un libro correctamente.
def test_delete_libro():
    """
    Crea un libro, lo elimina y verifica que ya no se puede recuperar por el endpoint.
    """
    post_response = client.post("/libros/", json={
        "isbn": 1234567890123,
        "titulo": "El Quijote",
        "autor": "Cervantes",
        "editorial": "Espasa",
        "precio": 19.99
    })
    libro_id = post_response.json()["id"]
    delete_response = client.delete(f"/libros/{libro_id}")
    assert delete_response.status_code == 204  # Verifica que fue eliminado
    get_response = client.get(f"/libros/{libro_id}")
    assert get_response.status_code == 404  # Verifica que ya no existe
