from http import HTTPStatus

from fastapi import FastAPI, HTTPException

from src.fast_zero.schemas import Message, UserSchema, UserPublic, UserDB, UserList

app = FastAPI()
database = []  # fake database


@app.get(
    '/', status_code=HTTPStatus.OK, response_model=Message
)  # endreço de acesso no website / -->> raíz do site
def read_root():
    return {'message': 'Ola, mundoo'}


@app.post('/users/', status_code=HTTPStatus.CREATED, response_model=UserPublic)
def create_users(user: UserSchema):
    user_with_id = UserDB(id=len(database) + 1, **user.model_dump())
    database.append(user_with_id)

    return user_with_id

@app.get('/users/', response_model=UserList)
def read_user():
    return {'users': database}

@app.put('/users/{user_id}', response_model=UserPublic)
def update_user(user_id: int, user: UserSchema):
    if user_id < 1 or user_id > len(database):
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='User not found'
        )

    user_with_id = UserDB(id=user_id, **user.model_dump())
    database[user_id - 1] = user_with_id

    return user_with_id

@app.delete('/users/{user_id}', response_model=Message)
def delete_user(user_id: int):
    if user_id < 1 or user_id > len(database):
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='User not found'
        )
    del database[user_id - 1]

    return {'message': 'User deleted'}
