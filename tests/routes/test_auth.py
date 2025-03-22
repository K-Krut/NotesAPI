from datetime import datetime
from datetime import timedelta

user = {
    'email': 'test_email@gmail.com',
    'password': 'testpassfortests',
}

non_existing_user = {
    'email': 'non_existing_user_email@gmail.com',
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


def test_login(client):
    response = client.post(
        "/api/auth/login",
        json=user
    )

    response_data = response.json()

    assert response.status_code == 200

    assert response_data.get('access_token')
    assert response_data.get('refresh_token')
    assert response_data.get('user').get('email') == user['email']



def test_login_non_existing_email(client):
    pass


def test_login_incorrect_password(client):
    pass


def test_token_refresh(client):
    pass


def test_token_refresh_expire(client):
    pass


def test_token_refresh_invalid_token(client):
    pass


def test_logout(client):
    pass


def test_logout_invalid_token(client):
    pass
