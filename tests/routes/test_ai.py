import pytest
from tests.data.ai import TEXT_SUMMARIZATION_TEST_DATA, USER_AI
from tests.data.auth import INVALID_JWT_TOKEN


@pytest.fixture(scope="module")
def test_ai_user_token(client):
    response_register = client.post("/api/auth/register", json=USER_AI)
    assert response_register.status_code == 200

    response = client.post("/api/auth/login", json=USER_AI)
    assert response.status_code == 200

    return response.json().get("access_token")


def test_summarize_text(client, test_ai_user_token):
    response = client.post(
        "/api/ai/text/summarize",
        json={"details": TEXT_SUMMARIZATION_TEST_DATA['details']},
        headers={"Authorization": f"Bearer {test_ai_user_token}"}
    )

    assert response.status_code == 200
    assert response.json().get('summary')


def test_summarize_text_without_token(client):
    response = client.post(
        "/api/ai/text/summarize",
        json={"details": TEXT_SUMMARIZATION_TEST_DATA["details"]}
    )
    assert response.status_code == 401


def test_summarize_text_invalid_token(client):
    response = client.post(
        "/api/ai/text/summarize",
        json={"details": TEXT_SUMMARIZATION_TEST_DATA["details"]},
        headers={"Authorization": f"Bearer {INVALID_JWT_TOKEN}"}
    )
    assert response.status_code == 401
