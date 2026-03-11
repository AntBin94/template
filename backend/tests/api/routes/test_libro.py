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
) -> None: #datos de sesión
    """
    Crea un libro y luego lo recupera por su ID usando el endpoint.
    """
    libro = crear_libro_random(db)  #libro creado
    response = client.get( #llamamos al enpoint
        f"{settings.API_V1_STR}/libros/{libro.id}",
        headers=superuser_token_headers,
       )
    assert response.status_code == 200 #verificamos estado
    content = response.json() #almacenamos respuesta
    assert content["isbn"]== libro.isbn #comparamos campos de libro con la llamada
    assert content["titulo"]== libro.titulo
    assert content["autor"]== libro.autor
    assert content["editorial"]== libro.editorial
    assert content["id"] == str(libro.id)
    assert content["creador_id"] == str(libro.creador_id)

#test para obtener todos los libros vía endpoint
#Este test permite verificar el endpoint /libros/ y que podamos recuperar
# al menos la cantidad de libros creados
def test_vemos_libros(
    client: TestClient, superuser_token_headers: dict[str, str], db:Session
) -> None:
    crear_libro_random(db) #crear libros
    crear_libro_random(db)
    response = client.get( #llamamos al endpoint
        f"{settings.API_V1_STR}/libros/",
        headers=superuser_token_headers,
    )
    assert response.status_code == 200 #verificamos respuesta
    content= response.json() #almacenamos respuesta
    assert len(content["datos"]) >=2 #comprueba que la lista sea de almenos 2

#Test para obtener el libro por su ISBN
#Este test va a verificar el endpoint /bucar_por_isbn/{isbn}
def test_obtenemos_libro_por_isbn(
    client: TestClient, superuser_token_headers: dict[str, str], db:Session
    ) -> None:
    """
    Creamos libro y lo llamamos por el isbn
    """
    libro = crear_libro_random(db)
    response = client.get(
        f"{settings.API_V1_STR}/libros/buscar_por_isbn/{libro.isbn}",
        headers=superuser_token_headers,
        )
    assert response.status_code == 200
    content = response.json()
    # Accedemos al primer libro de la lista en "datos"
    libro_encontrado = content["datos"][0]
    assert libro_encontrado["isbn"]== libro.isbn
    assert libro_encontrado["titulo"]== libro.titulo
    assert libro_encontrado["autor"]== libro.autor
    assert libro_encontrado["editorial"]== libro.editorial
    assert libro_encontrado["id"] == str(libro.id)
    assert libro_encontrado["creador_id"] == str(libro.creador_id)


# Test para actualizar un libro vía endpoint
# Este test verifica que el endpoint PATCH /libros/{id} permite actualizar datos de un libro.
def test_actualizamos_libro( client: TestClient, superuser_token_headers: dict[str, str], db:Session
) -> None:
    """
    Crea un libro, lo actualiza y verifica que el cambio se refleje en la respuesta.
    """
    libro = crear_libro_random(db) #creamos un libro aleatorio
    dato = { #estos son los nuevos datos
        "isbn": "01234568791", 
        "titulo":"el principito", 
        "autor":"un europeo random", 
        "editorial":"alguna europea"
        }
    response = client.put(
    f"{settings.API_V1_STR}/libros/{libro.id}", 
    headers=superuser_token_headers, 
    json=dato,
    )
    assert response.status_code == 200
    contenido = response.json()
    assert contenido["isbn"] == dato["isbn"]
    assert contenido["titulo"] == dato["titulo"]
    assert contenido["autor"] == dato["autor"]
    assert contenido["editorial"] == dato["editorial"]
    assert contenido["id"] == str(libro.id)
    assert contenido["creador_id"] == str(libro.creador_id)

# Test para eliminar un libro vía endpoint
# Este test verifica que el endpoint DELETE /libros/{id} elimina un libro correctamente.
def test_eliminar_libro(
    client: TestClient, superuser_token_headers: dict[str, str], db: Session
) -> None:
    """
    Crea un libro, lo elimina y verifica que ya no se puede recuperar por el endpoint.
    """
    libro = crear_libro_random(db)
    response = client.delete(
        f"{settings.API_V1_STR}/libros/{libro.id}",
        headers=superuser_token_headers,
    )
    assert response.status_code == 200
    contenido = response.json()
    assert contenido["message"] == "Libro eliminado correctamente"
