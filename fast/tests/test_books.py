from http import HTTPStatus

from fast.schemas import BookPublic
from tests.factories import BookFactory

# from fast.utils.sanitize import sanitize


def test_read_books(client):
    response = client.get('/books')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'books': []}


def test_read_books_with_books(client, book, author):
    book_schema = BookPublic.model_validate(book).model_dump()
    response = client.get('/books')
    assert response.json() == {'books': [book_schema]}


def test_read_book(client, book):
    response = client.get('/books/1')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'year': 1942,
        'title': book.title,
        'id': 1,
        'author_id': 1,
    }


def test_read_book_not_found_404(client, book, author):
    response = client.get('/books/2')
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'Book not found'}


def test_list_books_should_return_5_books(session, client, author, token):
    expected_books = 5
    session.bulk_save_objects(BookFactory.create_batch(5))
    session.commit()

    response = client.get(
        '/books/',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert len(response.json()['books']) == expected_books


def test_list_books_filter_title_should_return_3_books(
    session, client, token, author
):
    expected_books = 3
    session.bulk_save_objects(BookFactory.create_batch(3, title='fundação'))
    session.bulk_save_objects(
        BookFactory.create_batch(2, title='o fim da eternidade')
    )

    session.commit()

    response = client.get(
        '/books/?title=fund',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert len(response.json()['books']) == expected_books


def test_list_books_filter_year_should_return_3_books(
    session, client, token, author
):
    expected_books = 3
    session.bulk_save_objects(BookFactory.create_batch(3, year=1950))
    session.bulk_save_objects(BookFactory.create_batch(2, year=1999))

    session.commit()

    response = client.get(
        '/books/?year=1950',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert len(response.json()['books']) == expected_books


def test_list_books_filter_title_and_year_should_return_2_books(
    session, client, token, author
):
    expected_books = 2
    session.bulk_save_objects(BookFactory.create_batch(3, year=1950))
    session.bulk_save_objects(
        BookFactory.create_batch(2, year=1983, title='a cor da magia')
    )

    session.commit()

    response = client.get(
        '/books/?year=1983&title=magia',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert len(response.json()['books']) == expected_books


def test_create_book(client, author, token):
    response = client.post(
        '/books/',
        headers={'Authorization': f'Bearer {token}'},
        json={'year': 1949, 'title': '1984', 'author_id': author.id},
    )
    assert response.json() == {
        'year': 1949,
        'title': '1984',
        'author_id': author.id,
        'id': 1,
    }


def test_create_book_no_author_404(client, token):
    response = client.post(
        '/books/',
        headers={'Authorization': f'Bearer {token}'},
        json={'year': 1942, 'title': 'Fundação', 'author_id': 1},
    )
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {
        'detail': 'Author does not exist in the database'
    }


def test_create_book_empty_year_400(client, author, token):
    response = client.post(
        '/books',
        headers={'Authorization': f'Bearer {token}'},
        json={'year': None, 'title': 'Fundação', 'author_id': 1},
    )
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


def test_create_book_empty_title_400(client, author, token):
    response = client.post(
        '/books',
        headers={'Authorization': f'Bearer {token}'},
        json={'year': 1942, 'title': '   ', 'author_id': 1},
    )
    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json() == {'detail': 'Empty field'}


def test_create_book_empty_author_id_400(client, author, token):
    response = client.post(
        '/books',
        headers={'Authorization': f'Bearer {token}'},
        json={'year': 1942, 'title': 'Fundação', 'author_id': None},
    )
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


def test_create_book_conflict_409(client, token, author, book):
    response = client.post(
        '/books',
        headers={'Authorization': f'Bearer {token}'},
        json={'year': 1942, 'title': 'Fundação', 'author_id': 1},
    )
    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json() == {
        'detail': 'Book from this author already exists'
    }


def test_patch_book(client, token, author, book):
    response = client.patch(
        f'/books/{book.id}',
        headers={'Authorization': f'Bearer {token}'},
        json={'year': 1942, 'title': 'Segunda Fundação', 'author_id': 1},
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'year': 1942,
        'title': 'segunda fundação',
        'author_id': 1,
        'id': book.id,
    }


def test_patch_book_empty_string_400(client, token, author, book):
    response = client.patch(
        f'/books/{book.id}',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'title': '   ',
        },
    )
    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json() == {'detail': 'Empty string'}


def test_patch_book_conflict_409(client, token, author, book):
    response = client.patch(
        f'/books/{book.id}',
        headers={'Authorization': f'Bearer {token}'},
        json={'year': 1942, 'title': 'Fundação', 'author_id': 1},
    )
    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json() == {
        'detail': 'Book from this author already exists'
    }


def test_patch_book_no_author_404(client, token, book):
    response = client.patch(
        f'/books/{book.id}',
        headers={'Authorization': f'Bearer {token}'},
        json={'year': 1949, 'title': '1984', 'author_id': 2},
    )
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {
        'detail': 'Author does not exist in the database'
    }


def test_patch_book_not_found_404(client, token, author, book):
    response = client.patch(
        '/books/10',
        json={'year': 1942, 'title': 'Fundação', 'author_id': 1},
        headers={'Authorization': f'Bearer {token}'},
    )
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'Book not found.'}


def test_delete_book(session, client, token, author):
    book = BookFactory()

    session.add(book)
    session.commit()

    response = client.delete(
        f'/books/{book.id}', headers={'Authorization': f'Bearer {token}'}
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'message': 'Book has been deleted successfully.'
    }


def test_delete_book_not_found_404(client, token):
    response = client.delete(
        f'/books/{10}', headers={'Authorization': f'Bearer {token}'}
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'Book not found.'}
