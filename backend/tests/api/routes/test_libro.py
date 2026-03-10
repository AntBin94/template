import uuid

from fastapi.testclient import TestClient
from sqlmodel import Session

from app.core.config import settings
from tests.utils.libro import crear_libro_random

# Test para crear un libro vía endpoint
# Este test verifica que el endpoint /libros/ permite crear un libro correctamente.
def test_crear_libro(
    client: TestClient, superuser_token_headers: dict[str, str]
) -> None:
    data = {
        "isbn": "1234567890123",
        "titulo": "El Quijote",
        "autor": "Cervantes",
        "editorial": "Espasa",
        "precio": 19.99
        }
    response = client.post(f"{settings.API_V1_STR}/libros/", 
    headers = superuser_token_headers,
    json=data
    )
    assert response.status_code == 200  # Verifica el código de respuesta
    content = response.json()
    assert content["isbn"] == data["isbn"] #verifica el isbn
    assert content["titulo"] == data["titulo"]  # Verifica el título
    assert content["autor"] == data["autor"]    # Verifica el autor
    assert content["editorial"] == data["editorial"] #verificamos la editorial
    assert content["precio"] == data["precio"] #verificamos el precio
    assert "id" in content 
    assert "creador_id" in content

# Test para obtener un libro vía endpoint
# Este test verifica que el endpoint /libros/{id} permite recuperar un libro existente.
def test_vemos_libro(
    client: TestClient, superuser_token_headers: dict[str, str], db: Session
) -> None:
    """
    Crea un libro y luego lo recupera por su ID usando el endpoint.
    """
    libro = crear_libro_random(db)
    response = client.get(
        f"{settings.API_V1_STR}/libros/{libro.id}",
        headers=superuser_token_headers,
       )
    assert response.status_code == 200
    content = response.json()
    assert content["isbn"]== libro.isbn
    assert content["titulo"]== libro.titulo
    assert content["autor"]== libro.autor
    assert content["editorial"]== libro.editorial
    assert content["id"] == str(libro.id)
    assert content["creador_id"] == str(libro.creador_id)

#test para obtener todos los libros vía endpoint
#Este test permite verificar el endpoint /libros/
def test_vemos_libros(
    client: TestClient, superuser_token_headers: dict[str, str], db:Session
) -> None:
    crear_libro_random(db)
    crear_libro_random(db)
    response = client.get(
        f"{settings.API_V1_STR}/libros/",
        headers=superuser_token_headers,
    )
    assert response.status_code == 200
    content= response.json()
    assert len(content["datos"]) >=2

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
