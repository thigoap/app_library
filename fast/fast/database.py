from http import HTTPStatus

from fastapi import HTTPException
from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session

from fast.models import Author, User
from fast.settings import Settings
from fast.utils.sanitize import sanitize

engine = create_engine(Settings().DATABASE_URL)


def get_session():  # pragma: no cover
    with Session(engine) as session:
        yield session


def check_existing_users(session, user):
    db_user = session.scalar(
        select(User).where(
            (User.username == sanitize(user.username))
            | (User.email == user.email)
        )
    )
    if db_user:
        if db_user.username == sanitize(user.username):
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail='Username already exists',
            )
        elif db_user.email == user.email:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail='Email already exists',
            )


def check_existing_users_patch(session, user):
    if user.username:
        db_user = session.scalar(
            select(User).where((User.username == sanitize(user.username)))
        )
        if db_user:
            if db_user.username == sanitize(user.username):
                raise HTTPException(
                    status_code=HTTPStatus.BAD_REQUEST,
                    detail='Username already exists',
                )
    if user.email:
        db_user = session.scalar(
            select(User).where((User.email == user.email))
        )
        if db_user:
            if db_user.email == user.email:
                raise HTTPException(
                    status_code=HTTPStatus.BAD_REQUEST,
                    detail='Email already exists',
                )


def check_existing_authors(session, author):
    db_author = session.scalar(
        select(Author).where((Author.name == sanitize(author.name)))
    )
    if db_author:
        if db_author.name == sanitize(author.name):
            raise HTTPException(
                status_code=HTTPStatus.CONFLICT,
                detail='Author already exists',
            )
