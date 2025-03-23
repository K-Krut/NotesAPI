import pytest
from app.services import users as user_services



def test_validate_user_limits(mock_db, user_sample):
    mock_db.query().filter().first.return_value = user_sample

    user = user_services.validate_user_limits(mock_db, user_sample.id)

    assert user.email == user_sample.email
    assert user.id == user_sample.id


