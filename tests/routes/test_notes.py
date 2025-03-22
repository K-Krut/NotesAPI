import pytest


@pytest.fixture
def test_user_token(client):
    response = client.post(
        "/api/auth/register",
        json={
            "email": "test_notes@gmail.com",
            "password": "pass12345"
        }
    )

    response_data = response.json()
    return response_data.get("access_token")


def test_create_note(client):
    pass


def test_create_note_version(client):
    pass


def test_get_notes(client):
    pass


def test_get_note(client):
    pass


def test_get_note_history(client):
    pass


def test_update_note_fully(client):
    pass


def test_update_note(client):
    pass


def test_delete_note(client):
    pass
