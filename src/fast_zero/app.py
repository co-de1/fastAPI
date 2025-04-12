from http import HTTPStatus

from fastapi import FastAPI

from src.fast_zero.schemas import Message
from src.fast_zero.routers import users, auth


app = FastAPI()

app.include_router(users.router)
app.include_router(auth.router)


@app.get(
    '/', status_code=HTTPStatus.OK, response_model=Message
)  # endregion de access no website / -->> root of wesite
def read_root():
    return {'message': 'Ola, mundoo'}
