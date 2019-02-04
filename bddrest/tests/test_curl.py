from bddrest import FirstCall, Call
from bddrest.documentary.curl import CURL

def test_curl():
    params = dict(
        url='example.com',
        query=dict(c=1),
        verb='POST',
        form=dict(a=1),
        headers=['A: B'],
        content_type='text/plain',
        authorization='TOKEN'
    )

    assert str(CURL(**params)) == 'curl ' \
        '-X POST ' \
        '-F "a=1" ' \
        '-H "A: B" ' \
        '-H "Content-Type: text/plain" ' \
        '-H "Authorization: TOKEN" ' \
        '-- "example.com?c=1"'

    assert str(CURL(nerds_readable=True, **params)) == 'curl ' \
        '-XPOST ' \
        '-F"a=1" ' \
        '-H"A: B" ' \
        '-H"Content-Type: text/plain" ' \
        '-H"Authorization: TOKEN" ' \
        '-- "example.com?c=1"'

