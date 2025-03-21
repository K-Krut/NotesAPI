from http.client import HTTPException
from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.crud.users import get_user_by_id
from app.models.models import User


def get_user_remaining_requests(user: User):
    return user.ai_requests_limit - user.ai_requests_used


def validate_user_limits(db: Session, user_id: int) -> User:
    user_record = get_user_by_id(db, user_id)

    if not user_record:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User not found")

    user_remaining_requests = get_user_remaining_requests(user_record)

    if user_remaining_requests == 0:
        raise HTTPException(status_code=status.HTTP_429_TOO_MANY_REQUESTS, detail="Monthly ai requests limit reached")

    return user_record
