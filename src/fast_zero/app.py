from http import HTTPStatus

from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from src.fast_zero.schemas import Message, UserSchema, UserPublic, UserList
from models import User
from  database import get_session

app = FastAPI()

@app.get(
    '/', status_code=HTTPStatus.OK, response_model=Message
)  # endreço de acesso no website / -->> raíz do site
def read_root():
    return {'message': 'Ola, mundoo'}


@app.post('/users/', status_code=HTTPStatus.CREATED, response_model=UserPublic)
def create_users(user: UserSchema, session=Depends(get_session)):
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
            username=user.username, email=user.email, password=user.password
        )
        session.add(db_user)
        session.commit()
        session.refresh(db_user)

        return db_user

@app.get('/users/', response_model=UserList)
def read_user(
        limit: int = 10,
        skip: int = 0,
        session: Session=Depends(get_session)
):
    user = session.scalars(
        select(User).limit(limit).offset(skip)
    )
    return {'users': user}

@app.put('/users/{user_id}', response_model=UserPublic)
def update_user(
        user_id: int, user: UserSchema,
        session: Session=Depends(get_session)
):
    db_user = session.scalar(select(User).where(User.id == user_id))

    if not db_user:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='User not found'
        )
    db_user.email = user.email
    db_user.username = user.username
    db_user.password = user.password

    session.add(db_user)
    session.commit()
    session.refresh(db_user)

    return db_user

@app.delete('/users/{user_id}', response_model=Message)
def delete_user(
        user_id: int,
        session: Session=Depends(get_session)
):
    db_user = session.scalar(select(User).where(User.id == user_id))

    if not db_user:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='User not found'
        )

    session.delete(db_user)
    session.commit()

    return {"message": "User deleted"}