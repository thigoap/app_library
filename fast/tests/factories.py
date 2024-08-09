import factory
import factory.fuzzy

from fast.models import Author, Book


class AuthorFactory(factory.Factory):
    class Meta:
        model = Author

    name = factory.Sequence(lambda n: f'George{n}')


class BookFactory(factory.Factory):
    class Meta:
        model = Book

    year = factory.Faker('pyint')
    title = factory.Sequence(lambda n: f'Fundação{n}')
    author_id = 1
