import uuid
import logging
from datetime import datetime, timedelta

from jose import jwt, JWTError
from sqlalchemy.orm import Session

from app.core.config import settings
from app.models.models import Token

logger = logging.getLogger(__name__)


def create_token(db: Session, token_data: dict) -> None:
    token_record = Token(
        jti=token_data.get('jti'),
        user_id=token_data.get('id'),
        expires_at=datetime.fromtimestamp(token_data.get('exp'))
    )
    db.add(token_record)
    db.commit()


def generate_token(db: Session, user_id: int, expires_time: int) -> str:
    token_data = {
        "id": user_id,
        "exp": (datetime.utcnow() + timedelta(minutes=expires_time)).timestamp(),
        "jti": str(uuid.uuid4())
    }
    token = jwt.encode(token_data, settings.SECRET_KEY, settings.ALGORITHM)

    create_token(db, token_data)

    return token


def create_access_token(db: Session, user_id: int) -> str:
    return generate_token(db, user_id, expires_time=settings.ACCESS_TOKEN_EXPIRE)


def create_refresh_token(db: Session, user_id: int) -> str:
    return generate_token(db, user_id, expires_time=settings.REFRESH_TOKEN_EXPIRE)


def get_token_by_jti(db: Session, jti: str) -> Token | None:
    return db.query(Token).filter(Token.jti == jti).first()


def blacklist_token(db: Session, token_jti: str) -> None:
    token = get_token_by_jti(db, token_jti)
    if token:
        token.is_blacklisted = True
        db.commit()
        db.refresh(token)


def validate_token(db: Session, token: str) -> dict | None:
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=settings.ALGORITHM)
        jti: str = payload.get('jti')
        exp: int = payload.get('exp')
        user_id: int = payload.get('id')
        token_record = get_token_by_jti(db, jti)

        if exp > datetime.utcnow().timestamp() and not token_record.is_blacklisted:
            return {'jti': jti, 'user_id': user_id}
        return None
    except JWTError:
        logger.error(f'----#ERROR (JWTError) in validate_token()')
        return None
