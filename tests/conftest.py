import pytest
from fastapi.testclient import TestClient
from app.main import app
from tests.data.notes import NOTES_USER, NOTES_USER_2


@pytest.fixture(scope="module")
def client():
    return TestClient(app)


@pytest.fixture(scope="module")
def test_user_token(client):

    response_register = client.post("/api/auth/register", json=NOTES_USER)
    assert response_register.status_code == 200

    response = client.post("/api/auth/login", json=NOTES_USER)
    assert response.status_code == 200

    return response.json().get("access_token")


@pytest.fixture(scope="module")
def test_second_user_token(client):

    response_register = client.post("/api/auth/register", json=NOTES_USER_2)
    assert response_register.status_code == 200

    response = client.post("/api/auth/login", json=NOTES_USER_2)
    assert response.status_code == 200

    return response.json().get("access_token")
