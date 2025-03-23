from unittest.mock import MagicMock

import pytest
from fastapi.testclient import TestClient

from app.auth.hash import get_hashed_password
from app.main import app
from app.models.models import User
from app.schemas.users import UserSchema
from tests.data.auth import FAKE_USER


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
    )


@pytest.fixture(scope="module")
def user_schema_sample() -> UserSchema:
    return UserSchema(
        email=FAKE_USER['email'],
        password=FAKE_USER['password'],
    )