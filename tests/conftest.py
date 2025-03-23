from unittest.mock import MagicMock

import pytest
from fastapi.testclient import TestClient
from app.main import app


@pytest.fixture(scope="module")
def client():
    return TestClient(app)


@pytest.fixture()
def mock_db():
    return MagicMock()



def test_get_user_by_email_found(mock_db):
    fake_user = User(id=1, email="test@example.com")
    mock_db.query().filter().first.return_value = fake_user

    user = crud_users.get_user_by_email(mock_db, "test@example.com")

    assert user == fake_user
    mock_db.query.assert_called_once()


def test_get_user_by_email_not_found(mock_db):
    mock_db.query().filter().first.return_value = None

    user = crud_users.get_user_by_email(mock_db, "notfound@example.com")

    assert user is None


def test_get_user_by_id_found(mock_db):
    fake_user = User(id=1, email="test@example.com")
    mock_db.query().filter().first.return_value = fake_user

    user = crud_users.get_user_by_id(mock_db, 1)

    assert user == fake_user


def test_get_user_by_id_not_found(mock_db):
    mock_db.query().filter().first.return_value = None

    user = crud_users.get_user_by_id(mock_db, 999)

    assert user is None


def test_update_user(mock_db):
    user = User(id=1, email="old@example.com")
    fields = {"email": "updated@example.com", "ai_requests_limit": 5}

    updated = crud_users.update_user(mock_db, user, fields)

    assert updated.email == "updated@example.com"
    assert updated.ai_requests_limit == 5

    mock_db.commit.assert_called_once()
    mock_db.refresh.assert_called_once()
