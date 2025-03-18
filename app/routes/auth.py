from fastapi import APIRouter
from app.schemas.users import UserResponse

router = APIRouter()


@router.post("/register", response_model=UserResponse)
def register():
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

