from typing import Any
from fastapi import APIRouter, Depends
from schemas.users import UserResponse, User
from sqlalchemy.orm import Session
from database import get_db


router = APIRouter()


@router.post("/register", response_model=UserResponse)
def register(user: User, db: Session = Depends(get_db)) -> Any:
    pass


@router.post("/login", response_model=UserResponse)
def login():
    pass


@router.post("/logout")
def logout():
    pass


@router.post("/token/refresh")
def token_refresh():
    pass

