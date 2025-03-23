import pytest
from tests.data.ai import TEXT_SUMMARIZATION_TEST_DATA


def test_summarize_text_success(client, test_user_token):
    response = client.post(
        "/api/ai/text/summarize",
        json={"details": TEXT_SUMMARIZATION_TEST_DATA['details']},
        headers={"Authorization": f"Bearer {test_user_token}"}
    )

    assert response.status_code == 200
    assert response.json().get('summary') == TEXT_SUMMARIZATION_TEST_DATA['summary']

