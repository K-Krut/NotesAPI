import uuid
from datetime import datetime, timedelta
from jose import jwt
from sqlalchemy.orm import Session

from app.core.config import settings
from app.models.models import Token


def create_token(db: Session, token_data: dict):
    token_record = Token(
        jti=token_data.get('jti'),
        user_id=token_data.get('id'),
        expires_at=datetime.fromtimestamp(token_data.get('exp'))
    )
    db.add(token_record)
    db.commit()


def generate_token(db: Session, user_id: int, expires_time: int):
    token_data = {
        "id": user_id,
        "exp": (datetime.utcnow() + timedelta(minutes=expires_time)).timestamp(),
        "jti": str(uuid.uuid4())
    }
    token = jwt.encode(token_data, settings.SECRET_KEY, settings.ALGORITHM)

    create_token(db, token_data)

    return token


def create_access_token(db: Session, user_id: int):
    return generate_token(db, user_id, expires_time=settings.ACCESS_TOKEN_EXPIRE)


def create_refresh_token(db: Session, user_id: int):
    return generate_token(db, user_id, expires_time=settings.REFRESH_TOKEN_EXPIRE)
