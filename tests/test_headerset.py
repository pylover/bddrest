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


def test_iteration():
    headers = HeaderSet(('foo: bar', 'baz: QUX', 'foo: corge'))
    assert list(headers.items()) == [
        ('foo', 'bar,corge'),
        ('baz', 'QUX'),
    ]


# def test_insert():
#     expected_headers = [('A', 'B'), ('C', 'D')]
#     headers = HeaderSet()
#     headers.insert(0, ('C', 'D'))
#     headers.insert(0, ('A', 'B'))
#     assert expected_headers == headers
#
#     headers = HeaderSet()
#     headers.insert(0, 'C: D')
#     headers.insert(0, 'A: B')
#     assert expected_headers == headers
#
#     headers = HeaderSet()
#     headers.insert(0, 'C', 'D')
#     headers.insert(0, 'A', 'B')
#     assert expected_headers == headers
#
#
# def test_setitem_getitem_delitem():
#     expected_headers = [('A', 'B'), ('C', 'D')]
#     # setitem
#     headers = HeaderSet(['A: F'])
#     headers[0] = 'A: B'
#     headers['C'] = 'D'
#     assert expected_headers == headers
#
#     # getitem
#     assert expected_headers[0] == headers[0]
#     assert 'B' == headers['A']
#     assert 'B' == headers['a']
#
#     # delitem
#     del headers[0]
#     del headers['C']
#     assert [] == headers
#
#
# def test_in_operator():
#     headers = HeaderSet(['A: F'])
#     assert 'A' in headers
#     assert 'a' in headers
#     assert 'A: F' in headers
#
#
# def test_extend():
#     expected_headers = [('A', 'B'), ('C', 'D')]
#
#     headers = HeaderSet(['A: B'])
#     headers.extend(['C: D'])
#     assert expected_headers == headers
#
#
# def test_regex_match():
#     headers = HeaderSet(['Content-Type: application/json;utf-8'])
#     assert re.compile('^content-type: .*', re.I) in headers
#
#
# def test_remove():
#     headers = HeaderSet([('A', 'B'), ('C', 'D')])
#     headers.remove('A')
#     headers.remove('C: D')
#     assert [] == headers
#
#
# def test_copy():
#     headers = HeaderSet([('A', 'B'), ('C', 'D')])
#     headers_copy = headers.copy()
#     assert isinstance(headers_copy, HeaderSet)
#
#     headers_copy.remove('A')
#     assert headers is not headers_copy
#     assert 'A' in headers
#     assert 'A' not in headers_copy
