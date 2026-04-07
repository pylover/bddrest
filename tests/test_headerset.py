import re

from bddrest import HeaderSet


def test_constructor():
    headers = HeaderSet(('A: B', 'C: D', 'A: B'))
    assert headers == {'a': 'B,B', 'c': 'D'}

    headers = HeaderSet({'A': 'B,B', 'C': 'D'})
    assert headers == {'a': 'B,B', 'c': 'D'}


def test_append():
    headers = HeaderSet()
    headers.append(('Foo', 'bar'))
    headers.append('baz: QUX')
    headers.append('quux', 'thud')
    headers.append('foo', 'corge')
    assert headers == {
        'foo': 'bar,corge',
        'baz': 'QUX',
        'quux': 'thud'
    }

    assert headers['FOO'] == 'bar,corge'


def test_iteration():
    headers = HeaderSet(('foo: bar', 'baz: QUX', 'foo: corge'))
    assert list(headers.items()) == [
        ('foo', 'bar,corge'),
        ('baz', 'QUX'),
    ]


def test_in_operator():
    headers = HeaderSet(['A: F'])
    assert 'A' in headers
    assert 'a' in headers


def test_regex_match():
    headers = HeaderSet(['Content-Type: application/json;utf-8'])
    assert re.compile('^content-type$', re.I) in headers
