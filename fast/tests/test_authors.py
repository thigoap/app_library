from http import HTTPStatus

from fast.schemas import AuthorPublic
from tests.factories import AuthorFactory

# from fast.utils.sanitize import sanitize


def test_read_authors(client):
    response = client.get('/authors')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'authors': []}


def test_read_authors_with_authors(client, author):
    author_schema = AuthorPublic.model_validate(author).model_dump()
    response = client.get('/authors')
    assert response.json() == {'authors': [author_schema]}


def test_read_author(client, author):
    response = client.get('/authors/1')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'name': author.name,
        'id': 1,
    }


def test_read_author_not_found_404(client, author):
    response = client.get('/authors/2')
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'Author not found'}


def test_list_authors_should_return_5_authors(session, client, token):
    expected_authors = 5
    session.bulk_save_objects(AuthorFactory.create_batch(5))
    session.commit()

    response = client.get(
        '/authors/',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert len(response.json()['authors']) == expected_authors


def test_list_authors_filter_name_should_return_3_authors(
    session, client, token
):
    expected_authors = 3
    session.bulk_save_objects(AuthorFactory.create_batch(3, name='george'))
    session.bulk_save_objects(AuthorFactory.create_batch(2, name='isaac'))

    session.commit()

    response = client.get(
        '/authors/?name=geo',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert len(response.json()['authors']) == expected_authors


def test_create_author(client, token):
    response = client.post(
        '/authors/',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'name': 'George Orwell',
        },
    )
    assert response.json() == {
        'id': 1,
        'name': 'george orwell',
    }


def test_create_author_empty_string_400(client, token):
    response = client.post(
        '/authors',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'name': '   ',
        },
    )
    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json() == {'detail': 'Empty string'}


def test_create_author_conflict_409(client, token, author):
    response = client.post(
        '/authors',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'name': 'George Orwell',
        },
    )
    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json() == {'detail': 'Author already exists'}


def test_patch_author(client, token, author):
    response = client.patch(
        f'/authors/{author.id}',
        headers={'Authorization': f'Bearer {token}'},
        json={'name': 'Isaac Asimov'},
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json()['name'] == 'isaac asimov'


def test_patch_author_empty_string_400(client, token, author):
    response = client.patch(
        f'/authors/{author.id}',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'name': '   ',
        },
    )
    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json() == {'detail': 'Empty string'}


def test_patch_author_conflict_409(client, token, author):
    response = client.patch(
        f'/authors/{author.id}',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'name': 'George Orwell',
        },
    )
    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json() == {'detail': 'Author already exists'}


def test_patch_author_not_found_404(client, token):
    response = client.patch(
        '/authors/10',
        json={'name': 'Isaac'},
        headers={'Authorization': f'Bearer {token}'},
    )
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'Author not found.'}


def test_delete_author(session, client, token):
    author = AuthorFactory()

    session.add(author)
    session.commit()

    response = client.delete(
        f'/authors/{author.id}', headers={'Authorization': f'Bearer {token}'}
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'message': 'Author has been deleted successfully.'
    }


def test_delete_author_not_found_404(client, token):
    response = client.delete(
        f'/authors/{10}',
        headers={'Authorization': f'Bearer {token}'}
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'Author not found.'}
