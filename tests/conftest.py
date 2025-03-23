import random
from unittest.mock import MagicMock

import pytest
from fastapi.testclient import TestClient

from app.auth.hash import get_hashed_password
from app.main import app
from app.models.models import User
from app.schemas.users import UserSchema
from tests.data.auth import FAKE_USER
from tests.data.notes import NOTES_USER_2, NOTES_USER, NOTES_DATA, NOTE, ANALYTICS_USER


@pytest.fixture(scope="module")
def client():
    return TestClient(app)


@pytest.fixture()
def mock_db():
    return MagicMock()


@pytest.fixture(scope="module")
def user_sample() -> User:
    return User(
        id=1,
        email=FAKE_USER['email'],
        password=get_hashed_password(FAKE_USER['password']),
        ai_requests_limit=50,
        ai_requests_used=0
    )


@pytest.fixture(scope="module")
def user_schema_sample() -> UserSchema:
    return UserSchema(
        email=FAKE_USER['email'],
        password=FAKE_USER['password'],
    )


@pytest.fixture(scope="module")
def test_user_token(client):

    response_register = client.post("/api/auth/register", json=NOTES_USER)
    assert response_register.status_code == 200

    response = client.post("/api/auth/login", json=NOTES_USER)
    assert response.status_code == 200

    return response.json().get("access_token")


@pytest.fixture(scope="module")
def test_analytics_user_token(client):

    response_register = client.post("/api/auth/register", json=ANALYTICS_USER)
    assert response_register.status_code == 200

    response = client.post("/api/auth/login", json=ANALYTICS_USER)
    assert response.status_code == 200

    return response.json().get("access_token")


@pytest.fixture(scope="module")
def test_second_user_token(client):

    response_register = client.post("/api/auth/register", json=NOTES_USER_2)
    assert response_register.status_code == 200

    response = client.post("/api/auth/login", json=NOTES_USER_2)
    assert response.status_code == 200

    return response.json().get("access_token")


@pytest.fixture(scope="module")
def bulk_create_notes(client, test_user_token):
    notes = []

    for i in NOTES_DATA:
        response = client.post(
            "/api/notes/",
            json={
                "name": i.get('name'),
                "details": i.get('details'),
            },
            headers={"Authorization": f"Bearer {test_user_token}"}
        )
        assert response.status_code == 200
        notes.append(response.json())

    return notes


@pytest.fixture(scope="module")
def bulk_create_notes_analytics(client, test_analytics_user_token):

    notes = []

    for i in NOTES_DATA:
        response = client.post(
            "/api/notes/",
            json={
                "name": i.get('name'),
                "details": i.get('details'),
            },
            headers={"Authorization": f"Bearer {test_analytics_user_token}"}
        )
        assert response.status_code == 200
        notes.append(response.json())

    return notes


@pytest.fixture(scope="module")
def note_with_versions(client, test_user_token):
    headers = {"Authorization": f"Bearer {test_user_token}"}

    original = client.post(
        "/api/notes/",
        json=NOTE,
        headers=headers
    ).json()
    parent_id = original["id"]
    versions = [original]

    for _ in range(3):
        data = random.choice(NOTES_DATA)
        version = client.post(
            "/api/notes/",
            json={
                "name": data['name'],
                "details": data["details"],
                "parent_id": parent_id
            },
            headers=headers
        ).json()
        versions.append(version)
        parent_id = version["id"]

    return {
        "original": versions[0],
        "versions": versions[1:],
        "latest": versions[-1]
    }


@pytest.fixture(scope="module")
def note_for_tests(client, test_user_token):
    response = client.post(
        "/api/notes/",
        json=NOTE,
        headers={"Authorization": f"Bearer {test_user_token}"}
    )

    assert response.status_code == 200
    return response.json()
