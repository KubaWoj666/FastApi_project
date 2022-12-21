import pytest
from jose import jwt
from app import schemas
from app.config import settings


def test_create_user(client):
    response = client.post("/users/", json={"email": "test@gmail.com", "password": "hasło"})
    new_user = schemas.UserOut(**response.json())
    assert new_user.email == "test@gmail.com"
    assert response.status_code == 201


def test_login_user(test_user, client):
    response = client.post("/login", data={"username": "test@gmail.com", "password": "hasło"})
    login_response = schemas.Token(**response.json())
    pyload = jwt.decode(login_response.access_token, settings.secret_key, algorithms=[settings.algorithm])
    id = pyload.get("user_id")
    assert id == test_user['id']
    assert login_response.token_type == 'Bearer'
    assert response.status_code == 200


@pytest.mark.parametrize("email, password, status_code",[
    ("wrong@email", "hasło", 403),
    ("test@gmail.com", "wrong_password", 403),
    ("wrong@email", "wrong_password", 403),
    (None, "hasło", 422),
    ("test@gmail.com", None, 422)
])
def test_incorrect_login(test_user, client, email, password, status_code):
    response = client.post("/login", data={"username": email, "password": password})
    assert response.status_code == status_code