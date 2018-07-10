import unittest

from bddrest.specification import Given, When


def test_when_setters_deleters():
    basecall = Given(
        'Base call for testing When class',
        url='/apiv1/devices/id: 1',
    )

    when = When(
        basecall,
        title='Testing the When class',
        url='/apiv1/books/isbn: abc/pages/page: 3?highlight=false',
        verb='POST',
        form=dict(a='b'),
        headers=['A: B'],
        content_type='text/plain',
        as_='Admin',
        extra_environ=dict(A='B')
    )
    assert '/apiv1/books/:isbn/pages/:page' == when.url
    assert dict(isbn='abc', page='3') == when.url_parameters
    assert dict(highlight='false') == when.query
    assert dict(a='b') == when.form
    assert 'POST' == when.verb
    assert 'A' in when.headers
    assert 'text/plain' == when.content_type
    assert 'Admin' == when.as_
    del when.url_parameters
    del when.verb
    del when.headers
    del when.query
    del when.content_type
    del when.as_
    del when.extra_environ
    del when.form

    assert dict(id='1') == when.url_parameters
    assert 'GET' == when.verb
    assert when.headers is None
    assert when.query is None
    assert when.form is None
    assert when.content_type is None
    assert when.as_ is None
    assert when.extra_environ is None

