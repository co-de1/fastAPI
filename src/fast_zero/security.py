from zoneinfo import ZoneInfo
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends
from pwdlib import PasswordHash
from jwt import encode
from datetime import datetime, timedelta

from database import get_session
from sqlalchemy.orm import Session

pwd_context = PasswordHash.recommended()
oauth2_schema = OAuth2PasswordBearer(tokenUrl='token')

SECRET_KEY = 'Your-secret-key'
ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data_payload: dict) -> str:
    to_encode = data_payload.copy()
    expire = datetime.now(tz=ZoneInfo('UTC')) + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )

    to_encode.update({'exp': expire})

    encoded_jwt = encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt


def get_current_user(
    session: Session = Depends(get_session),
    token: str = Depends(oauth2_schema),
): ...
