from datetime import datetime, timedelta, timezone

from jose import JWTError, jwt

from app.core.config import settings

from sqlalchemy.orm import Session

from app.core.security import verify_password
from app.models.user import User

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from app.core.database import get_db

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# from app.services.auth_service import (
#     decode_access_token,
#     get_user_by_email,
# )

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
    user = get_user_by_email(
        db,
        email
    )

    if not user:
        return None

    if not verify_password(
        password, 
        user.password_hash
    ):
        return None

    return user

def get_user_by_email(
    db: Session,
    email: str
):
    return (
        db.query(User)
        .filter(User.email == email)
        .first()
    )

def decode_access_token(token: str):
    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms = [settings.ALGORITHM]
        )

        return payload

    except JWTError:
        return None

def get_current_user(
        token: str = Depends(oauth2_scheme),
        db: Session = Depends(get_db)
):
    payload = decode_access_token(token)

    if payload is None:
        raise HTTPException(
            status_code = 401,
            detail="Invalid token"
        )

    email = payload.get("sub")
    user = get_user_by_email(db, email)

    if user is None:
        raise HTTPException(
            status_code = 401,
            detail = "User not found"
        )

    return user