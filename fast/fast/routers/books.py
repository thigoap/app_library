from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.orm import Session

from fast.database import (
    check_existing_author_by_id,
    check_existing_books_from_author,
    get_session,
)
from fast.models import Book, User
from fast.schemas import BookList, BookPublic, BookSchema, BookUpdate, Message
from fast.security import get_current_user
from fast.utils.sanitize import sanitize

router = APIRouter()

Session = Annotated[Session, Depends(get_session)]
CurrentUser = Annotated[User, Depends(get_current_user)]

router = APIRouter(prefix='/books', tags=['books'])


@router.post('/', response_model=BookPublic)
def create_book(
    book: BookSchema,
    user: CurrentUser,
    session: Session,
):
    check_existing_books_from_author(session, book)
    check_existing_author_by_id(session, book)

    if not sanitize(book.title) or not book.year or not book.author_id:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Empty field',
        )

    db_book = Book(
        year=book.year, title=sanitize(book.title), author_id=book.author_id
    )

    session.add(db_book)
    session.commit()
    session.refresh(db_book)

    return db_book


@router.get('/', response_model=BookList)
def list_books(  # noqa
    session: Session,
    title: str = Query(None),
    year: int = Query(None),
    offset: int = Query(None),
    limit: int = Query(None),
):
    query = select(Book)

    if title:
        query = query.filter(Book.title.contains(sanitize(title)))
    if year:
        query = query.filter(Book.year == year)

    books = session.scalars(query.offset(offset).limit(limit)).all()

    return {'books': books}


@router.get('/{book_id}', response_model=BookPublic)
def read_book(book_id: int, session: Session):
    db_book = session.scalar(select(Book).where(Book.id == book_id))
    if not db_book:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='Book not found'
        )

    return db_book


@router.patch('/{book_id}', response_model=BookPublic)
def patch_book(
    book_id: int,
    session: Session,
    user: CurrentUser,
    book: BookUpdate,
):
    db_book = session.scalar(select(Book).where(Book.id == book_id))

    if not db_book:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Book not found.'
        )
    if not sanitize(book.title):
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Empty string',
        )

    check_existing_books_from_author(session, book)
    check_existing_author_by_id(session, book)

    if book.year:
        db_book.year = book.year
    if book.title:
        db_book.title = sanitize(book.title)
    if book.author_id:
        db_book.author_id = book.author_id

    session.commit()
    session.refresh(db_book)

    return db_book


@router.delete('/{book_id}', response_model=Message)
def delete_book(book_id: int, session: Session, user: CurrentUser):
    book = session.scalar(select(Book).where(Book.id == book_id))

    if not book:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='Book not found.'
        )

    session.delete(book)
    session.commit()

    return {'message': 'Book has been deleted successfully.'}
