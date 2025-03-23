import pytest

from app.auth.hash import get_hashed_password
from app.crud.users import create_user, get_user_by_email, get_user_by_id
from app.models.models import User
from app.schemas.users import UserSchema

FAKE_USER = {
    'email': "fake@gmail.com",
    'password': "secret",
}


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


def test_create_user(mock_db, user_schema_sample):
    user = create_user(mock_db, user_schema_sample)

    assert isinstance(user, User)
    assert user.email == user_schema_sample.email
    assert user.password != user_schema_sample.password

    mock_db.add.assert_called_once()
    mock_db.commit.assert_called_once()
    mock_db.refresh.assert_called_once()


def test_get_user_by_email(user_sample, mock_db):
    mock_db.query().filter().first.return_value = user_sample

    user = get_user_by_email(mock_db, user_sample.email)

    assert user is not None
    assert user.email == user_sample.email



def test_get_user_by_id(mock_db, user_sample):
    mock_db.query().filter().first.return_value = user_sample

    user = get_user_by_id(mock_db, user_sample.id)

    assert user is not None
    assert user.email == user_sample.email


def test_update_user():
    pass
