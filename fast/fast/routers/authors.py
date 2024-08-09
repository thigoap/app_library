from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.orm import Session

from fast.database import check_existing_authors, get_session
from fast.models import Author, User
from fast.schemas import (
    AuthorList,
    AuthorPublic,
    AuthorSchema,
    AuthorUpdate,
    Message,
)
from fast.security import get_current_user
from fast.utils.sanitize import sanitize

router = APIRouter()

Session = Annotated[Session, Depends(get_session)]
CurrentUser = Annotated[User, Depends(get_current_user)]

router = APIRouter(prefix='/authors', tags=['authors'])


@router.post('/', response_model=AuthorPublic)
def create_author(
    author: AuthorSchema,
    user: CurrentUser,
    session: Session,
):
    check_existing_authors(session, author)

    if not sanitize(author.name):
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Empty string',
        )

    db_author = Author(name=sanitize(author.name))
    session.add(db_author)
    session.commit()
    session.refresh(db_author)

    return db_author


@router.get('/', response_model=AuthorList)
def list_authors(  # noqa
    session: Session,
    name: str = Query(None),
    offset: int = Query(None),
    limit: int = Query(None),
):
    query = select(Author)

    if name:
        query = query.filter(Author.name.contains(sanitize(name)))

    authors = session.scalars(query.offset(offset).limit(limit)).all()

    return {'authors': authors}


@router.get('/{author_id}', response_model=AuthorPublic)
def read_author(author_id: int, session: Session):
    db_author = session.scalar(select(Author).where(Author.id == author_id))
    if not db_author:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='Author not found'
        )

    return db_author


@router.patch('/{author_id}', response_model=AuthorPublic)
def patch_author(
    author_id: int,
    session: Session,
    user: CurrentUser,
    author: AuthorUpdate,
):
    db_author = session.scalar(select(Author).where(Author.id == author_id))

    if not db_author:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='Author not found.'
        )
    if not sanitize(author.name):
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Empty string',
        )

    check_existing_authors(session, author)

    # for key, value in author.model_dump(exclude_unset=True).items():
    #     setattr(db_author, key, value)
    if author.name:
        db_author.name = sanitize(author.name)

    session.commit()
    session.refresh(db_author)

    return db_author


@router.delete('/{author_id}', response_model=Message)
def delete_author(author_id: int, session: Session, user: CurrentUser):
    author = session.scalar(select(Author).where(Author.id == author_id))

    if not author:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='Author not found.'
        )

    session.delete(author)
    session.commit()

    return {'message': 'Author has been deleted successfully.'}
