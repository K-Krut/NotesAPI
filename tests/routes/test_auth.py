from datetime import datetime
from datetime import timedelta

user = {
    'email': 'test_email@gmail.com',
    'password': 'testpassfortests',
}


def test_register(client):
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



def test_register_with_existing_email(client):
    response = client.post(
        "/api/auth/register",
        json=user
    )
    assert response.status_code == 400


