import json

from bddrest import Given, when, response, given


def wsgi_application(environ, start_response):
    form = json.load(environ['wsgi.input'])
    start_response('200 OK', [
        ('Content-Type', 'application/json;charset=utf-8'),
    ])
    yield json.dumps(form).encode()


def test_update_json_fields():
    call = dict(
        title='test remove form fields',
        url='/apiv1/devices/name: SM-12345678/id: 1',
        verb='POST',
        json=dict(
            a='1',
            b=2
        )
    )

    with Given(wsgi_application, **call):
        assert response.status == '200 OK'
        assert response.json == dict(a='1', b=2)

        when(
            'Adding new field',
            json=given + dict(c=3)
        )
        assert response.json == dict(a='1', b=2, c=3)

        when(
            'Updating a field with None',
            json=given | dict(b=None)
        )
        assert response.json == dict(a='1', b=None)

        when(
            'Removing a field',
            json=given - 'a'
        )
        assert response.json == dict(b=2)

