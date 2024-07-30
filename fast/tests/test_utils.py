from fast.utils.sanitize import sanitize


def test_sanitize():
    sanitized = sanitize('user     ')
    assert sanitized == 'user'


def test_sanitize_empty_string():
    sanitized = sanitize('      ')
    assert not sanitized
