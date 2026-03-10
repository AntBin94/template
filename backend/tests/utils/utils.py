import random
import string

from fastapi.testclient import TestClient

from app.core.config import settings


def random_lower_string() -> str:
    return "".join(random.choices(string.ascii_lowercase, k=32))


def random_email() -> str:
    return f"{random_lower_string()}@{random_lower_string()}.com"


def get_superuser_token_headers(client: TestClient) -> dict[str, str]:
    login_data = {
        "username": settings.FIRST_SUPERUSER,
        "password": settings.FIRST_SUPERUSER_PASSWORD,
    }
    r = client.post(f"{settings.API_V1_STR}/login/access-token", data=login_data)
    tokens = r.json()
    a_token = tokens["access_token"]
    headers = {"Authorization": f"Bearer {a_token}"}
    return headers

#agregamos una función random para un ISBN
def random_isbn() -> str:
    """Devuelve un número aleatorio entre 10 y 13 dígitos pero sale 
    como string."""
    length = random.randint(10, 13)
    return "".join(random.choices("0123456789", k=length))

#agregamos una función para un float random
def random_float(min_value: float = 0.0, max_value: float = 100.0) -> float:
    """Devuelve un número float aleatorio entre 0 y 100"""
    return random.uniform(min_value, max_value)
    