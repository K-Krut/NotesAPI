import pytest
from app.services import users as user_services
from tests.conftest import user_sample


def test_validate_user_limits(mock_db, user_sample):
    mock_db.query().filter().first.return_value = user_sample
    user = user_services.validate_user_limits(mock_db, user_sample.id)

    assert user.email == user_sample.email
    assert user.id == user_sample.id


def test_validate_user_limits_reached(mock_db, user_sample):
    user = user_sample
    user.ai_requests_used = 50
    mock_db.query().filter().first.return_value = user

    with pytest.raises(Exception) as exc:
        user_services.validate_user_limits(mock_db, user.id)

    assert exc.value.status_code == 429



def test_update_user_limits(mock_db, user_sample):
    used_requests = user_sample.ai_requests_used + 1

    user = user_services.update_user_limits(mock_db, user_sample)

    assert user.ai_requests_used == used_requests
