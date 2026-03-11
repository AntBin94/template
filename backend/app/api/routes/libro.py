import uuid
from typing import Any

from fastapi import APIRouter, HTTPException
from sqlmodel import col, func, select

from app.api.deps import CurrentUser, SessionDep
from app.models import (
    Libro,
    LibroCrear,
    LibroActualizar,
    LibroPublico,
    LibrosPublicos,
    Message
)

router = APIRouter(prefix="/libros", tags=["libros"])

# Obtener la información de los libros con lista
@router.get("/", response_model=LibrosPublicos)
def leer_libros(
    session: SessionDep, current_user: CurrentUser, skip: int = 0, limit: int = 100
) -> Any:
    """
    Obtenemos los libros.
    """
    if current_user.is_superuser:
        count_statement = select(func.count()).select_from(Libro)
        count = session.exec(count_statement).one()
        statement = (
            select(Libro).order_by(col(Libro.id).desc()).offset(skip).limit(limit)
        )
        libros = session.exec(statement).all()
    else:
        count_statement = (
            select(func.count())
            .select_from(Libro)
            .where(Libro.creador_id == current_user.id)
        )
        count = session.exec(count_statement).one()
        statement = (
            select(Libro)
            .where(Libro.creador_id == current_user.id)
            .order_by(col(Libro.id).desc())
            .offset(skip)
            .limit(limit)
        )
        libros = session.exec(statement).all()
    return LibrosPublicos(datos=libros, contador=count)

#Buscamos el libro por ID interno
@router.get("/{id}", response_model=LibroPublico)
def leer_libro(session: SessionDep, current_user: CurrentUser, id: uuid.UUID) -> Any:
    """
    Get libro by ID.
    """
    libro = session.get(Libro, id)
    if not libro:
        raise HTTPException(status_code=404, detail="Libro no encontrado")
    if not current_user.is_superuser and (libro.creador_id != current_user.id):
        raise HTTPException(status_code=403, detail="No tienes permisos suficientes")
    return libro

#Buscamos el libro por su ISBN
@router.get("/buscar_por_isbn/{isbn}", response_model=LibrosPublicos)
def leer_libro_por_isbn(session: SessionDep, current_user: CurrentUser, isbn: str) -> Any:
    """
    Obtener libros por el ISBN.
    """
    statement = select(Libro).where(Libro.isbn == isbn)
    libros = session.exec(statement).all()
    if not libros:
        raise HTTPException(status_code=404, detail="No se encontraron libros con ese ISBN")
    # Filtrar por permisos
    if not current_user.is_superuser:
        libros = [libro for libro in libros if libro.creador_id == current_user.id]
        if not libros:
            raise HTTPException(status_code=403, detail="No tienes permisos suficientes")
    return LibrosPublicos(datos=libros, contador=len(libros))

#Registramos los libros
@router.post("/", response_model=LibroPublico)
def crear_libro(
    *, session: SessionDep, current_user: CurrentUser, libro_in: LibroCrear
) -> Any:
    """
    Registramos un nuevo libro.
    """
    libro = Libro.model_validate(libro_in, update={"creador_id": current_user.id})
    session.add(libro)
    session.commit()
    session.refresh(libro)
    return libro

#Actualización de los datos de un Libro
@router.put("/{id}", response_model=LibroPublico)
def actualizar_libro(
    *,
    session: SessionDep,
    current_user: CurrentUser,
    id: uuid.UUID,
    libro_in: LibroActualizar,
) -> Any:
    """
    Actualizamos el libro.
    """
    libro = session.get(Libro, id)
    if not libro:
        raise HTTPException(status_code=404, detail="Libro no encontrado")
    if not current_user.is_superuser and (libro.creador_id != current_user.id):
        raise HTTPException(status_code=403, detail="No tienes permisos suficientes")
    update_dict = libro_in.model_dump(exclude_unset=True)
    libro.sqlmodel_update(update_dict)
    session.add(libro)
    session.commit()
    session.refresh(libro)
    return libro

#Eliminamos un libro de nuestro registro
@router.delete("/{id}")
def borrar_libro(
    session: SessionDep, current_user: CurrentUser, id: uuid.UUID
) -> Message:
    """
    Borramos el libro.
    """
    libro = session.get(Libro, id)
    if not libro:
        raise HTTPException(status_code=404, detail="Libro no encontrado")
    if not current_user.is_superuser and (libro.creador_id != current_user.id):
        raise HTTPException(status_code=403, detail="No tienes permisos suficientes")
    session.delete(libro)
    session.commit()
    return Message(message="Libro eliminado correctamente")
