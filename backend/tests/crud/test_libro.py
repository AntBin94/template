import pytest
from app.models import Libro, LibroCrear
from app.crud import libro_crud  # Ajusta el import si tu CRUD tiene otro nombre

@pytest.mark.usefixtures("db")
def test_crear_libro(db):
    """
    Crea un libro y verifica que los datos guardados sean correctos.
    Utiliza el fixture db para la sesión de base de datos.
    """
    nuevo_libro = libro_crud.crear_libro(
        db=db,
        libro=LibroCrear(
            isbn=1234567890123,
            titulo="El Quijote",
            autor="Cervantes",
            editorial="Espasa",
            precio=19.99
        )
    )
    assert nuevo_libro.titulo == "El Quijote"  # Verifica el título
    assert nuevo_libro.autor == "Cervantes"    # Verifica el autor
    assert nuevo_libro.precio == 19.99         # Verifica el precio

@pytest.mark.usefixtures("db")
def test_leer_libro(db):
    """
    Crea un libro y luego lo recupera por su ID para verificar que los datos sean correctos.
    Utiliza el fixture db para la sesión de base de datos.
    """
    libro = libro_crud.crear_libro(
        db=db,
        libro=LibroCrear(
            isbn=1234567890123,
            titulo="El Quijote",
            autor="Cervantes",
            editorial="Espasa",
            precio=19.99
        )
    )
    libro_recuperado = libro_crud.get_libro(db_session, libro.id)
    assert libro_recuperado is not None
    assert libro_recuperado.titulo == "El Quijote"

@pytest.mark.usefixtures("db")
def test_actualizar_libro(db):
    """
    Crea un libro, lo actualiza y verifica que el cambio se haya guardado.
    Utiliza el fixture db para la sesión de base de datos.
    """
    libro = libro_crud.crear_libro(
        db=db,
        libro=LibroCrear(
            isbn=1234567890123,
            titulo="El Quijote",
            autor="Cervantes",
            editorial="Espasa",
            precio=19.99
        )
    )
    libro_actualizado = libro_crud.actualizar_libro(
        db=db,
        libro_id=libro.id,
        precio=25.00
    )
    assert libro_actualizado.precio == 25.00  # Verifica el nuevo precio

@pytest.mark.usefixtures("db")
def test_eliminar_libro(db):
    """
    Crea un libro, lo elimina y verifica que ya no se puede recuperar.
    Utiliza el fixture db para la sesión de base de datos.
    """
    libro = libro_crud.crear_libro(
        db=db,
        libro=LibroCrear(
            isbn=1234567890123,
            titulo="El Quijote",
            autor="Cervantes",
            editorial="Espasa",
            precio=19.99
        )
    )
    libro_crud.eliminar_libro(db, libro.id)
    libro_recuperado = libro_crud.get_libro(db, libro.id)
    assert libro_recuperado is None  # Verifica que el libro fue eliminado
