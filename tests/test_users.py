from fastapi.testclient import TestClient
import jwt
import pytest

from app.config import settings
from app.models import User


# ------------------------------  Sign Up Route Tests ---------------------------------

def test_signup(client: TestClient):
    response = client.post(
        '/signup/',
        json={"username": "Aporva002", "email": "Aporvanayar002@gmail.com", "password": "ronin1331"}
        )

    data = response.json()
    assert response.status_code == 201
    assert data['username'] == "Aporva002"
    assert data['email'] == "Aporvanayar002@gmail.com"
    assert data['first_name'] is None 
    assert data['last_name'] is None
    assert data['id'] is not None
    assert data['active'] == True


@pytest.mark.parametrize("_username_, _email_, _password_, _status_code_", [
    ("Aporva001", "Aporvanayar001@gmail.com", "nanobots", 400),
    (None, "Aporvanayar001@gmail.com", "nanobots", 422),
    ("Aporva001", None, "nanobots", 422),
    ("Aporva001", "Aporvanayar001@gmail.com", None, 422)
])
def test_unsuccessfull_signup(client: TestClient, dummy_user1: User, _username_: str , _email_: str, _password_: str, _status_code_: int):
    response = client.post(
        '/signup/',
        json={"username": _username_, "email": _email_, "password": _password_}
    )

    assert response.status_code == _status_code_


# ------------------------------  Log In Route Tests ---------------------------------

def test_login(client: TestClient, dummy_user1: User):
    response = client.post(
        '/login/',
        data={"username": dummy_user1.username, "password": "nanobots"}
    )

    form_data = response.json()
    payload = jwt.decode(form_data["access_token"], settings.secret_key, algorithms=[settings.algorithm])
    username = payload.get("sub")
    
    assert response.status_code == 200
    assert username == dummy_user1.username
    assert form_data["token_type"] == "bearer"

def test_login_unsuccessfull(client: TestClient):
    response = client.post(
        '/login/',
        data={"username": "Aprova001", "password": "nanobots"}
    )

    assert response.status_code == 401

@pytest.mark.parametrize("_username_, _password_, _status_code_", [
    ("Aporva001", "wrong_passwd", 401),
    ("wrong_username", "nanobots", 401)
])
def test_login_badrequests(client: TestClient, dummy_user1: User, _username_: str, _password_: str, _status_code_: int):
    response = client.post(
        '/login/',
        data={"username": _username_, "password": _password_}
    )

    assert response.status_code == _status_code_


# ------------------------------  User Profile Route Tests ---------------------------------

def test_read_users_me(authorized_client1: TestClient, dummy_user1: User):
    response = authorized_client1.get('/users/me/')

    data = response.json()

    assert response.status_code == 200
    assert data['username'] == dummy_user1.username
    assert data['email'] == dummy_user1.email
    assert data['first_name'] == dummy_user1.first_name  
    assert data['last_name'] == dummy_user1.first_name
    assert data['id'] == dummy_user1.id
    assert data['active'] == dummy_user1.active

def test_read_users_me_unauthorized(client: TestClient):
    response = client.get('/users/me/')

    assert response.status_code == 401

