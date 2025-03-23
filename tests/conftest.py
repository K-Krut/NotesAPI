import pytest
from fastapi.testclient import TestClient
from app.main import app
from tests.data.notes import NOTES_USER, NOTES_USER_2


@pytest.fixture(scope="module")
def client():
    return TestClient(app)

