from http.client import HTTPException
from typing import Any
from fastapi import APIRouter, Depends, HTTPException
from app.schemas.users import UserResponse, UserSchema
from sqlalchemy.orm import Session
from app.database import get_db
from app.crud.users import get_user_by_email, create_user

router = APIRouter()


@router.post("/register", response_model=UserResponse)
def register(user: UserSchema, db: Session = Depends(get_db)) -> Any:
    check_user = get_user_by_email(db, email=user.email)

    if check_user:
        raise HTTPException(
            status_code=400,
            detail=f"User with '${user.email}' email already registered",
        )
    return create_user(db, user)


@router.post("/login", response_model=UserResponse)
def login():
    pass


@router.post("/logout")
def logout():
    pass


@router.post("/token/refresh")
def token_refresh():
    pass

