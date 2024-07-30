from sqlalchemy import select

from fast.models import Author, User


def test_create_user(session):
    new_user = User(username='username', password='secret', email='teste@test')
    session.add(new_user)
    session.commit()

    user = session.scalar(select(User).where(User.username == 'username'))

    assert user.username == 'username'


def test_create_author(session):
    new_author = Author(name='George Orwell')
    session.add(new_author)
    session.commit()

    author = session.scalar(
        select(Author).where(Author.name == 'George Orwell')
    )

    assert author.name == 'George Orwell'
