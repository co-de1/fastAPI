from fastapi import APIRouter, HTTPException, Depends
from src.fast_zero.schemas import Message, UserSchema, UserPublic, UserList
from sqlalchemy.orm import Session

from http import HTTPStatus
from typing import Annotated

from sqlalchemy import select
from src.fast_zero.models import User
from src.fast_zero.database import get_session
from src.fast_zero.security import (
    get_password_hash,
    get_current_user,
)

router = APIRouter(prefix='/users', tags=['users'])
T_Session = Annotated[Session, Depends(get_session)]
T_CurrentUser = Annotated[User, Depends(get_current_user)]


@router.get('/', response_model=UserList)
def read_user(
    session: T_Session,
    limit: int = 10,
    skip: int = 0,
):
    user = session.scalars(select(User).limit(limit).offset(skip))
    return {'users': user}


@router.post('/', status_code=HTTPStatus.CREATED, response_model=UserPublic)
def create_users(
    user: UserSchema,
    session: T_Session,
):
    db_user = session.scalar(
        select(User).where(
            (User.username == user.username) | (User.email == user.email)
        )
    )
    if db_user:
        if db_user.username == user.username:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail='Username already exists',
            )
        elif db_user.email == user.email:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail='Email already exists',
            )
    db_user = User(
        username=user.username,
        email=user.email,
        password=get_password_hash(user.password),
    )
    session.add(db_user)
    session.commit()
    session.refresh(db_user)

    return db_user


@router.put('/{user_id}', response_model=UserPublic)
def update_user(
    session: T_Session,
    user_id: int,
    user: UserSchema,
    current_user: T_CurrentUser,
):
    # db_user = session.scalar(select(User).where(User.id == user_id))

    if current_user.id != user_id:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST, detail='Not enough permissions'
        )
    current_user.email = user.email
    current_user.username = user.username
    current_user.password = get_password_hash(user.password)

    session.commit()
    session.refresh(current_user)

    return current_user


@router.delete('/{user_id}', response_model=Message)
def delete_user(
    session: T_Session,
    user_id: int,
    current_user: T_CurrentUser,
):
    if current_user.id != user_id:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST, detail='Not enough permissions'
        )

    # Verifica se o usuário existe no banco (opcional)
    db_user = session.get(User, user_id)
    if not db_user:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='User not found'
        )

    session.delete(current_user)
    session.commit()
    return {'message': 'User deleted'}
