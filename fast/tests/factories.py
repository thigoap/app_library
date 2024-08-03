import factory
import factory.fuzzy

from fast.models import Author


class AuthorFactory(factory.Factory):
    class Meta:
        model = Author

    name = factory.Sequence(lambda n: f'George{n}')
