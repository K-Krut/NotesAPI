from pydantic import EmailStr
from sqlalchemy.orm import Session
from app.models.models import User
from app.schemas.users import UserSchema, UserResponse
from app.auth.hash import get_hashed_password


def get_user_by_email(db: Session, email: EmailStr) -> User | None:
    return db.query(User).filter(User.email == email).first()


def create_user(db: Session, user: UserSchema) -> User:
    user_record = User(
        email=str(user.email),
        password=get_hashed_password(user.password),
    )
    db.add(user_record)
    db.commit()
    db.refresh(user_record)
    return user_record

