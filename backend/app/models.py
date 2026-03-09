from jwt.algorithms import NoneAlgorithm
import uuid
from datetime import datetime, timezone

from pydantic import EmailStr
from sqlalchemy import DateTime
from sqlmodel import Field, Relationship, SQLModel


def get_datetime_utc() -> datetime:
    return datetime.now(timezone.utc)


# Shared properties
class UserBase(SQLModel):
    email: EmailStr = Field(unique=True, index=True, max_length=255)
    is_active: bool = True
    is_superuser: bool = False
    full_name: str | None = Field(default=None, max_length=255)


# Properties to receive via API on creation
class UserCreate(UserBase):
    password: str = Field(min_length=8, max_length=128)


class UserRegister(SQLModel):
    email: EmailStr = Field(max_length=255)
    password: str = Field(min_length=8, max_length=128)
    full_name: str | None = Field(default=None, max_length=255)


# Properties to receive via API on update, all are optional
class UserUpdate(UserBase):
    email: EmailStr | None = Field(default=None, max_length=255)  # type: ignore
    password: str | None = Field(default=None, min_length=8, max_length=128)


class UserUpdateMe(SQLModel):
    full_name: str | None = Field(default=None, max_length=255)
    email: EmailStr | None = Field(default=None, max_length=255)


class UpdatePassword(SQLModel):
    current_password: str = Field(min_length=8, max_length=128)
    new_password: str = Field(min_length=8, max_length=128)


# Database model, database table inferred from class name
class User(UserBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    hashed_password: str
    created_at: datetime | None = Field(
        default_factory=get_datetime_utc,
        sa_type=DateTime(timezone=True),  # type: ignore
    )
    items: list["Item"] = Relationship(back_populates="owner", cascade_delete=True)
    libros: list["Libro"] = Relationship(back_populates="creador", cascade_delete=True)


# Properties to return via API, id is always required
class UserPublic(UserBase):
    id: uuid.UUID
    created_at: datetime | None = None


class UsersPublic(SQLModel):
    data: list[UserPublic]
    count: int


# Shared properties
class ItemBase(SQLModel):
    title: str = Field(min_length=1, max_length=255)
    description: str | None = Field(default=None, max_length=255)
    marca: str | None= Field(default=None, max_length=255)


# Properties to receive on item creation
class ItemCreate(ItemBase):
    pass


# Properties to receive on item update
class ItemUpdate(ItemBase):
    title: str | None = Field(default=None, min_length=1, max_length=255)  # type: ignore


# Database model, database table inferred from class name
class Item(ItemBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    created_at: datetime | None = Field(
        default_factory=get_datetime_utc,
        sa_type=DateTime(timezone=True),  # type: ignore
    )
    owner_id: uuid.UUID = Field(
        foreign_key="user.id", nullable=False, ondelete="CASCADE"
    )
    owner: User | None = Relationship(back_populates="items")

# Properties to return via API, id is always required
class ItemPublic(ItemBase):
    id: uuid.UUID
    owner_id: uuid.UUID
    created_at: datetime | None = None


class ItemsPublic(SQLModel):
    data: list[ItemPublic]
    count: int


# Generic message
class Message(SQLModel):
    message: str


# JSON payload containing access token
class Token(SQLModel):
    access_token: str
    token_type: str = "bearer"


# Contents of JWT token
class TokenPayload(SQLModel):
    sub: str | None = None


class NewPassword(SQLModel):
    token: str
    new_password: str = Field(min_length=8, max_length=128)


# Shared properties
class ProductoBase(SQLModel):
    nombre: str = Field(min_length=1, max_length=255)
    precio: float
    tamano: float

# Properties to receive on producto creation
class ProductoCreate(ProductoBase):
    pass

# Properties to receive on producto update
class ProductoUpdate(ProductoBase):
    nombre: str | None = Field(default=None, min_length=1, max_length=255)  # type: ignore
    precio: float | None = None
    tamano: float | None = None

# Database model, database table inferred from class name
class Producto(ProductoBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    created_at: datetime | None = Field(
        default_factory=get_datetime_utc,
        sa_type=DateTime(timezone=True),  # type: ignore
    )

# Properties to return via API, id is always required
class ProductoPublic(ProductoBase):
    id: int
    created_at: datetime | None = None

class ProductosPublic(SQLModel):
    data: list[ProductoPublic]
    count: int

# Creamos los campos base de la tabla
class LibroBase (SQLModel):
    isbn: int = Field(min_length=10, max_length=13)
    titulo: str = Field(min_length=1, max_length=255)
    autor: str = Field(min_length=1, max_length=255)
    editorial: str = Field(min_length=1, max_length=255)
    precio: float

# En esta recibimos los datos cuando creamos un nuevo producto
class LibroCrear(LibroBase):
    pass

# Aquí es para actualizar los datos del libro
class LibroActualizar(LibroBase):
    autor: str | None = Field(default=None, min_length=1, max_length=255)
    editorial: str | None = Field(default=None, min_length=1, max_length=255)
    precio: float | None = None

# Aquí ya definimos la tabla que se creará en la base de datos
class Libro(LibroBase, table=True):
     id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
     creador_id: uuid.UUID = Field(
        foreign_key="user.id", nullable=False, ondelete="CASCADE"
    )
     creador: User | None = Relationship(back_populates="libros")

# Aqui van las clases que devuelven la
# información al response de la api,
# el id siempre es requerido
class LibroPublico(LibroBase):
    id: uuid.UUID
    creador_id: uuid.UUID

class LibrosPublicos(SQLModel):
    datos: list[LibroPublico]
    contador: int

