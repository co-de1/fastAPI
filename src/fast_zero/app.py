from fastapi import FastAPI

app = FastAPI()


@app.get('/')  # endreço de acesso no website / -->> raíz do site
def read_root():
    return {'message': 'Ola, mundoo'}
