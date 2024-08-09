from http import HTTPStatus

from fastapi import FastAPI

from fast.routers import auth, authors, books, users
from fast.schemas import Message

app = FastAPI()

app.include_router(users.router)
app.include_router(auth.router)
app.include_router(authors.router)
app.include_router(books.router)


@app.get('/', status_code=HTTPStatus.OK, response_model=Message)
def read_root():
    return {'message': 'Hello world'}
