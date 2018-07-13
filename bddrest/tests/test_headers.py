import unittest
import re

from bddrest import HeaderSet


def test_constructor():
    expected_headers = [('A', 'B'), ('C', 'D')]
    headers = HeaderSet(('A: B', 'C: D'))
    assert expected_headers == headers

    headers = HeaderSet({'A': 'B', 'C': 'D'})
    assert expected_headers == headers

def test_append():
    expected_headers = [('A', 'B'), ('C', 'D')]
    headers = HeaderSet()
    headers.append(('A', 'B'))
    headers.append(('C', 'D'))
    assert expected_headers == headers

    headers = HeaderSet()
    headers.append('A: B')
    headers.append('C: D')
    assert expected_headers == headers

    headers = HeaderSet()
    headers.append('A', 'B')
    headers.append('C', 'D')
    assert expected_headers == headers

def test_insert():
    expected_headers = [('A', 'B'), ('C', 'D')]
    headers = HeaderSet()
    headers.insert(0, ('C', 'D'))
    headers.insert(0, ('A', 'B'))
    assert expected_headers == headers

    headers = HeaderSet()
    headers.insert(0, 'C: D')
    headers.insert(0, 'A: B')
    assert expected_headers == headers

    headers = HeaderSet()
    headers.insert(0, 'C', 'D')
    headers.insert(0, 'A', 'B')
    assert expected_headers == headers

def test_setitem_getitem_delitem():
    expected_headers = [('A', 'B'), ('C', 'D')]
    # setitem
    headers = HeaderSet(['A: F'])
    headers[0] = 'A: B'
    headers['C'] = 'D'
    assert expected_headers == headers

    # getitem
    assert expected_headers[0] == headers[0]
    assert 'B' == headers['A']
    assert 'B' == headers['a']

    # delitem
    del headers[0]
    del headers['C']
    assert [] == headers

def test_in_operator():
    headers = HeaderSet(['A: F'])
    assert 'A' in headers
    assert 'a' in headers
    assert 'A: F' in headers

def test_extend():
    expected_headers = [('A', 'B'), ('C', 'D')]

    headers = HeaderSet(['A: B'])
    headers.extend(['C: D'])
    assert expected_headers == headers

def test_regex_match():
    headers = HeaderSet(['Content-Type: application/json;utf-8'])
    assert re.compile('^content-type: .*', re.I) in headers

def test_remove():
    headers = HeaderSet([('A', 'B'), ('C', 'D')])
    headers.remove('A')
    headers.remove('C: D')
    assert [] == headers

