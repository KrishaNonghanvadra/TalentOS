from datetime import datetime, timedelta, timezone

from jose import jwt

from app.core.config import settings

from sqlalchemy.orm import Session

from app.core.security import verify_password
from app.models.user import User

def create_access_token(data: dict):

    to_encode = data.copy()

    expire = datetime.now(timezone.utc) + timedelta(
        minutes = settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )

    to_encode.update(
        {
            "exp": expire
        }
    )

    encoded_jwt = jwt.encode(
        to_encode,
        settings.SECRET_KEY,
        algorithm = settings.ALGORITHM
    )
    return encoded_jwt

def authenticate_user(
        db: Session,
        email: str,
        password: str
):
    user = db.query(User).filter(
        User.email == email
    ).first()

    if not user:
        return None

    if not verify_password(
        password, 
        user.password_hash
    ):
        return None

    return user