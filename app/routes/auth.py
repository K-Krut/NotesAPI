import logging
from http.client import HTTPException
from typing import Any
from fastapi import APIRouter, Depends, HTTPException, status
from app.schemas.users import UserResponse, UserSchema, LoginResponse, RefreshResponse, RefreshRequest, LogoutRequest
from sqlalchemy.orm import Session
from app.database import get_db
from app.crud.users import get_user_by_email, create_user
from app.auth.jwt import create_access_token, create_refresh_token, blacklist_token, validate_token
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
        logger.error(f'----#ERROR in /api/auth/register: {error}')
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
        logger.error(f'----#ERROR in /api/auth/login: {error}')
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error. {error}",
        )


@router.post("/logout")
def logout(tokens: LogoutRequest, db: Session = Depends(get_db)) -> Any:
    try:
        validated_access_token = validate_token(db, tokens.access_token)
        validated_refresh_token = validate_token(db, tokens.refresh_token)

        if not validated_access_token and not validated_refresh_token:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

        blacklist_token(db, validated_access_token.get('jti'))
        blacklist_token(db, validated_refresh_token.get('jti'))

        return Response(status_code=status.HTTP_200_OK)
    except HTTPException as error:
        raise error
    except Exception as error:
        logger.error(f'----#ERROR in /api/auth/logout: {error}')
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error. {error}",
        )


@router.post("/token/refresh")
def token_refresh(token: RefreshRequest, db: Session = Depends(get_db)) -> Any:
    try:
        validated_token = validate_token(db, token.refresh_token)

        if not validated_token:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

        blacklist_token(db, validated_token.get('jti'))

        return RefreshResponse(
            access_token=create_access_token(db, validated_token.get('user_id')),
            refresh_token=create_refresh_token(db, validated_token.get('user_id')),
        )
    except HTTPException as error:
        raise error
    except Exception as error:
        logger.error(f'----#ERROR in in /api/auth/token/refresh: {error}')
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error. {error}",
        )
