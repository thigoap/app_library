from datetime import datetime

from sqlalchemy import func
from sqlalchemy.orm import Mapped, mapped_column, registry

table_registry = registry()


@table_registry.mapped_as_dataclass
class User:
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    username: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str]
    email: Mapped[str] = mapped_column(unique=True)
    created_at: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now(), onupdate=func.now()
    )


@table_registry.mapped_as_dataclass
class Author:
    __tablename__ = 'authors'

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    name: Mapped[str]
    # books: Mapped[list['Book']] = relationship(
    #     init=False, back_populates='authors', cascade='all, delete-orphan'
    # )
    created_at: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now(), onupdate=func.now()
    )


# @table_registry.mapped_as_dataclass
# class Book:
#     __tablename__ = 'books'

#     id: Mapped[int] = mapped_column(init=False, primary_key=True)
#     year: Mapped[int]
#     title: Mapped[str]
#     author_id: Mapped[int] = mapped_column(ForeignKey('authors.id'))
#     author: Mapped[Author] = relationship(init=False, back_populates='books')
#     created_at: Mapped[datetime] = mapped_column(
#         init=False, server_default=func.now()
#     )
#     updated_at: Mapped[datetime] = mapped_column(
#         init=False, server_default=func.now(), onupdate=func.now()
#     )