from datetime import datetime

from pydantic import BaseModel, EmailStr


class UserSchema(BaseModel):
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    id: int
    email: EmailStr
    ai_requests_used: int
    ai_requests_limit: int
    ai_requests_reset: datetime

    class Config:
        from_attributes = True


class LoginResponse(BaseModel):
    access_token: str
    refresh_token: str
    user: UserResponse


class RefreshResponse(BaseModel):
    access_token: str
    refresh_token: str


class RefreshRequest(BaseModel):
    refresh_token: str


class LogoutRequest(BaseModel):
    access_token: str
    refresh_token: str
