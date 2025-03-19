import logging
from http.client import HTTPException
from typing import Any
from fastapi import APIRouter, Depends, HTTPException, status
from app.schemas.users import UserResponse, UserSchema, LoginResponse
from sqlalchemy.orm import Session
from app.database import get_db
from app.crud.users import get_user_by_email, create_user
from app.auth.jwt import create_access_token, create_refresh_token
from app.auth.hash import verify_password

router = APIRouter()
logger = logging.getLogger(__name__)


@router.post("/register", response_model=UserResponse)
def register(user: UserSchema, db: Session = Depends(get_db)) -> Any:
    try:
        check_user = get_user_by_email(db, email=user.email)

        if check_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"User with '{user.email}' email already registered",
            )
        return create_user(db, user)
    except HTTPException as error:
        raise error
    except Exception as error:
        logger.error(f'----#ERROR in register(): {error}')
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error. {error}",
        )


@router.post("/login", response_model=LoginResponse)
def login(user: UserSchema, db: Session = Depends(get_db)) -> Any:
    try:
        user_record = get_user_by_email(db, email=user.email)

        if not user_record:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"User with '{user.email}' email doesn't exist",
            )

        if not verify_password(user.password, user_record.password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=f"Incorrect password",
            )

        return LoginResponse(
            access_token=create_access_token(db, user_record.id),
            refresh_token=create_refresh_token(db, user_record.id),
            user=UserResponse.model_validate(user_record)
        )
    except HTTPException as error:
        raise error
    except Exception as error:
        logger.error(f'----#ERROR in register(): {error}')
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error. {error}",
        )


@router.post("/logout")
def logout():
    pass


@router.post("/token/refresh")
def token_refresh():
    pass
