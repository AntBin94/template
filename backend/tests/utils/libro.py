from sqlmodel import Session

from app import crud
from app.models import Libro, LibroCrear
from tests.utils.user import create_random_user
from tests.utils.utils import random_lower_string, random_isbn, random_float

def crear_libro_random(db: Session) -> Libro:
    user = create_random_user(db)
    creador_id = user.id
    assert creador_id is not None
    isbn = random_isbn()
    titulo = random_lower_string()
    autor = random_lower_string()
    editorial = random_lower_string()
    precio = random_float()
    libro_crear = LibroCrear(isbn=isbn, titulo=titulo, autor=autor, editorial=editorial, precio=precio)
    return crud.crear_libro(session= db, libro_crear=libro_crear, creador_id=creador_id)