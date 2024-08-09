from http import HTTPStatus

from fastapi import HTTPException
from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session

from fast.models import Author, Book, User
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
        # if db_author.name == sanitize(author.name):
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT,
            detail='Author already exists',
        )


def check_existing_books_from_author(session, book):
    db_book = session.scalar(
        select(Book).where(
            (Book.title == sanitize(book.title))
            & (Book.author_id == (book.author_id))
        )
    )
    if db_book:
        # if db_book.title == sanitize(book.title):
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT,
            detail='Book from this author already exists',
        )


def check_existing_author_by_id(session, book):
    db_author = session.scalar(
        select(Author).where((Author.id == book.author_id))
    )
    if not db_author:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Author does not exist in the database',
        )
