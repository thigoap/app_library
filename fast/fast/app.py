from http import HTTPStatus

from fastapi import FastAPI

from fast.routers import auth, authors, users
from fast.schemas import Message

app = FastAPI()

app.include_router(users.router)
app.include_router(auth.router)
app.include_router(authors.router)


@app.get('/', status_code=HTTPStatus.OK, response_model=Message)
def read_root():
    return {'message': 'Hello world'}
