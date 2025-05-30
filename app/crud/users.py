from pydantic import EmailStr
from sqlalchemy.orm import Session
from app.models.models import User
from app.schemas.users import UserSchema
from app.auth.hash import get_hashed_password


def get_user_by_email(db: Session, email: EmailStr) -> User | None:
    return db.query(User).filter(User.email == email).first()


def get_user_by_id(db: Session, user_id: int) -> User | None:
    return db.query(User).filter(User.id == user_id).first()


def create_user(db: Session, user: UserSchema) -> User:
    user_record = User(
        email=str(user.email),
        password=get_hashed_password(user.password),
    )
    db.add(user_record)
    db.commit()
    db.refresh(user_record)
    return user_record


def update_user(db: Session, user: User, fields: dict) -> User:
    for key, value in fields.items():
        setattr(user, key, value)

    db.commit()
    db.refresh(user)
    return user
