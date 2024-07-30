from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from fast.database import (
    check_existing_users,
    check_existing_users_patch,
    get_session,
)
from fast.models import User
from fast.schemas import (
    Message,
    UserList,
    UserPatch,
    UserPublic,
    UserSchema,
)
from fast.security import (
    get_current_user,
    get_password_hash,
)
from fast.utils.sanitize import sanitize

router = APIRouter(prefix='/users', tags=['users'])

Session = Annotated[Session, Depends(get_session)]
CurrentUser = Annotated[User, Depends(get_current_user)]


@router.post('/', status_code=HTTPStatus.CREATED, response_model=UserPublic)
def create_user(user: UserSchema, session: Session):
    if not sanitize(user.username):
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Empty string',
        )

    check_existing_users(session, user)
    hashed_password = get_password_hash(user.password)

    db_user = User(
        email=user.email,
        username=sanitize(user.username),
        password=hashed_password,
    )

    session.add(db_user)
    session.commit()
    session.refresh(db_user)

    return db_user


@router.get('/', response_model=UserList)
def read_users(session: Session, skip: int = 0, limit: int = 100):
    users = session.scalars(select(User).offset(skip).limit(limit)).all()
    return {'users': users}


@router.get('/{user_id}', response_model=UserPublic)
def read_user(user_id: int, session: Session):
    db_user = session.scalar(select(User).where(User.id == user_id))
    if not db_user:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='User not found'
        )

    return db_user


@router.patch('/{user_id}', response_model=UserPublic)
def patch_user(
    user_id: int,
    user: UserPatch,
    session: Session,
    current_user: CurrentUser,
):
    if current_user.id != user_id:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST, detail='Not enough permissions'
        )

    if user.username and not sanitize(user.username):
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Empty string',
        )

    check_existing_users_patch(session, user)
    hashed_password = get_password_hash(user.password)

    if user.username:
        current_user.username = sanitize(user.username)
    if user.password:
        current_user.password = hashed_password
    if user.email:
        current_user.email = user.email

    session.commit()
    session.refresh(current_user)

    return current_user


@router.put('/{user_id}', response_model=UserPublic)
def update_user(
    user_id: int,
    user: UserSchema,
    session: Session,
    current_user: CurrentUser,
):
    if current_user.id != user_id:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST, detail='Not enough permissions'
        )

    if not sanitize(user.username):
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Empty string',
        )

    check_existing_users(session, user)
    hashed_password = get_password_hash(user.password)

    current_user.username = sanitize(user.username)
    current_user.password = hashed_password
    current_user.email = user.email
    session.commit()
    session.refresh(current_user)

    return current_user


@router.delete('/{user_id}', response_model=Message)
def delete_user(
    user_id: int,
    session: Session,
    current_user: CurrentUser,
):
    if current_user.id != user_id:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST, detail='Not enough permissions'
        )

    session.delete(current_user)
    session.commit()

    return {'message': 'User deleted'}
