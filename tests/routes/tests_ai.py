import pytest
from tests.data.ai import TEXT_SUMMARIZATION_TEST_DATA
from tests.data.auth import INVALID_JWT_TOKEN


def test_summarize_text(client, test_user_token):
    response = client.post(
        "/api/ai/text/summarize",
        json={"details": TEXT_SUMMARIZATION_TEST_DATA['details']},
        headers={"Authorization": f"Bearer {test_user_token}"}
    )

    assert response.status_code == 200
    assert response.json().get('summary') == TEXT_SUMMARIZATION_TEST_DATA['summary']


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
