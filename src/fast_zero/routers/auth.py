from fastapi import APIRouter, HTTPException, Depends

from src.fast_zero.schemas import AuthToken  # modelo Pydantic
from typing import Annotated

from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select
from sqlalchemy.orm import Session

from src.fast_zero.models import User
from src.fast_zero.database import get_session
from src.fast_zero.security import (
    verify_password,
    create_access_token,
    get_current_user,
)

router = APIRouter(prefix='/auth', tags=['/auth'])
T_Session = Annotated[Session, Depends(get_session)]
T_OAuth2Form = Annotated[OAuth2PasswordRequestForm, Depends()]


@router.post('/token', response_model=AuthToken)
def login_for_access_token(session: T_Session, form_data: T_OAuth2Form):
    user = session.scalar(select(User).where(User.email == form_data.username))

    if not user or not verify_password(form_data.password, user.password):
        raise HTTPException(
            status_code=400, detail='Incorrect email or password'
        )

    access_token = create_access_token({'sub': user.email})

    return {'access_token': access_token, 'token_type': 'Bearer'}


@router.post('/refresh_token', response_model=AuthToken)
def refresh_access_token(
    session: T_Session,
    current_user: User = Depends(get_current_user),
):
    # Verifica se o usuário ainda existe no banco
    user = session.get(User, current_user.id)
    if not user:
        raise HTTPException(status_code=401, detail='User not found')

    new_access_token = create_access_token({'sub': user.email})
    return {
        'access_token': new_access_token,
        'token_type': 'Bearer',
    }  # Padronizado
