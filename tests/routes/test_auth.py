from datetime import datetime
from datetime import timedelta

from tests.data.auth import USER, NON_EXISTING_USER, INVALID_JWT_TOKEN


def test_register(client):
    response = client.post(
        "/api/auth/register",
        json=USER
    )
    response_data = response.json()

    assert response.status_code == 200
    assert response_data.get('email') == USER['email']
    assert response_data.get('ai_requests_used') == 0
    assert response_data.get('ai_requests_limit') == 50
    assert response_data.get('ai_requests_reset')[:10] == (datetime.today() + timedelta(days=30)).isoformat()[:10]


def test_register_with_existing_email(client):
    response = client.post(
        "/api/auth/register",
        json=USER
    )
    assert response.status_code == 400


def test_login(client):
    response = client.post(
        "/api/auth/login",
        json=USER
    )

    response_data = response.json()

    assert response.status_code == 200

    assert response_data.get('access_token')
    assert response_data.get('refresh_token')
    assert response_data.get('user').get('email') == USER['email']



def test_login_non_existing_email(client):
    response = client.post(
        "/api/auth/login",
        json=NON_EXISTING_USER
    )

    assert response.status_code == 400



def test_login_incorrect_password(client):
    response = client.post(
        "/api/auth/login",
        json={
            'email': USER['email'],
            'password': 'INCORRECT_PASSWORD_TEST'
        }
    )

    assert response.status_code == 401


# TODO test blacklisting
def test_token_refresh(client):
    login_response = client.post("/api/auth/login", json=USER)
    login_response_data = login_response.json()

    response = client.post(
        '/api/auth/token/refresh',
        json={"refresh_token": login_response_data.get('refresh_token')}
    )

    response_data = response.json()

    assert response.status_code == 200
    assert response_data.get('access_token')
    assert response_data.get('refresh_token')



def test_token_refresh_invalid_token(client):
    response = client.post(
        '/api/auth/token/refresh',
        json={"refresh_token": INVALID_JWT_TOKEN}
    )

    assert response.status_code == 401


def test_logout(client):
    login_response = client.post("/api/auth/login", json=USER)
    login_response_data = login_response.json()

    response = client.post(
        '/api/auth/token/refresh',
        json={
            "access_token": login_response_data.get('access_token'),
            "refresh_token": login_response_data.get('refresh_token')
        }
    )

    assert response.status_code == 200


def test_logout_invalid_token(client):
    response = client.post(
        '/api/auth/token/refresh',
        json={
            "access_token": INVALID_JWT_TOKEN,
            "refresh_token": INVALID_JWT_TOKEN
        }
    )

    assert response.status_code == 401
