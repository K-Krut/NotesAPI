from datetime import datetime
from datetime import timedelta


def test_register(client):
    user = {
        'email': 'test_email@gmail.com',
        'password': 'testpassfortests',
    }
    response = client.post(
        "/api/auth/register",
        json=user
    )
    response_data = response.json()

    assert response.status_code == 200
    assert response_data.get('email') == user['email']
    assert response_data.get('ai_requests_used') == 0
    assert response_data.get('ai_requests_limit') == 50
    assert response_data.get('ai_requests_reset')[:10] == (datetime.today() + timedelta(days=30)).isoformat()[:10]
