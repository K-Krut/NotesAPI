import pytest

from app.auth.hash import get_hashed_password
from app.crud.users import create_user, get_user_by_email
from app.models.models import User
from app.schemas.users import UserSchema

FAKE_USER = {
    'email': "fake@gmail.com",
    'password': "secret",
}


@pytest.fixture(scope="module")
def user_sample() -> User:
    return User(
        email=FAKE_USER['email'],
        password=get_hashed_password(FAKE_USER['password']),
    )


@pytest.fixture(scope="module")
def user_schema_sample() -> UserSchema:
    return UserSchema(
        email=FAKE_USER['email'],
        password=FAKE_USER['password'],
    )


def test_create_user(mock_db, user_schema_sample):
    user = create_user(mock_db, user_schema_sample)

    assert isinstance(user, User)
    assert user.email == user_schema_sample.email
    assert user.password != user_schema_sample.password

    mock_db.add.assert_called_once()
    mock_db.commit.assert_called_once()
    mock_db.refresh.assert_called_once()


def test_get_user_by_email(user_sample, mock_db):
    pass



def test_get_user_by_id():
    pass


def test_update_user():
    pass
