from http import HTTPStatus
from fastapi import FastAPI

from src.fast_zero.schemas import Message

app = FastAPI()


@app.get('/', status_code=HTTPStatus.OK, response_model=Message)  # endreço de acesso no website / -->> raíz do site
def read_root():
    return {'message': 'Ola, mundoo'}
