from zoneinfo import ZoneInfo
from src.fast_zero.models import User

import jwt
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException
from pwdlib import PasswordHash
from jwt import encode
from jwt.exceptions import DecodeError, ExpiredSignatureError
from datetime import datetime, timedelta

from src.fast_zero.database import get_session
from sqlalchemy.orm import Session
from sqlalchemy import select
from src.fast_zero.settings import Settings

pwd_context = PasswordHash.recommended()
oauth2_schema = OAuth2PasswordBearer(tokenUrl='auth/token')
settings = Settings()


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data_payload: dict) -> str:
    to_encode = data_payload.copy()
    expire = datetime.now(tz=ZoneInfo('UTC')) + timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )

    to_encode.update({'exp': expire})

    encoded_jwt = encode(
        to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM
    )

    return encoded_jwt


def get_current_user(
    session: Session = Depends(get_session),
    token: str = Depends(oauth2_schema),
):
    credentials_exception = HTTPException(
        status_code=401,
        detail='Could not validate credentials',
        headers={'WWW-Authenticate': 'Bearer'},
    )

    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        username: str = payload.get('sub')
        if not username:
            raise credentials_exception

    except ExpiredSignatureError:
        raise credentials_exception
    except DecodeError:
        raise credentials_exception

    user = session.scalar(select(User).where(User.email == username))

    if not user:
        raise credentials_exception

    return user
