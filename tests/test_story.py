import json
import tempfile

import pytest

from bddrest import Given, when, story, response, InvalidUrlParametersError, \
    CallVerifyError, Call, AlteredCall, Story, given

from . import multipart


def wsgi_application(environ, start_response):
    form, _ = multipart.parse_form_data(
        environ,
        charset="utf8",
        strict=True
    )

    try:
        # FIXME: Why x ^ 1234
        code = int(form['activationCode']) ^ 1234

    except ValueError:
        start_response(
            '400 Bad Request',
            [('Content-Type', 'text/plain;utf-8')]
        )
        return

    start_response('200 OK', [
        ('Content-Type', 'application/json;charset=utf-8'),
        ('X-Pagination-Count', '10')
    ])
    result = dict(
        secret='ABCDEF',
        code=code,
        query=environ.get('QUERY_STRING'),
        path=environ.get('PATH_INFO')
    )

    identity = environ.get('HTTP_AUTHORIZATION')
    if identity:
        result['identity'] = identity

    yield json.dumps(result).encode()


def test_given_when():
    call = dict(
        title='Binding and registering the device after verifying the '
              'activation code',
        description='As a new visitor I have to bind my device with '
                    'activation code and phone number',
        path='/apiv1/devices/name: SM-12345678',
        verb='POST',
        as_='visitor',
        query=dict(
            a=1,
            b=2
        ),
        form=dict(
            activationCode=['746727'],
            phone=['+9897654321']
        )
    )
    with Given(wsgi_application, **call) as s:
        assert s.response is response._resolver()
        assert response.status == '200 OK'
        assert response.status == 200
        assert 'secret' in response.json
        assert response.json['secret'] == 'ABCDEF'
        assert 'Bad Header' not in response.headers

        assert response.content_type == 'application/json'
        assert response.json == dict(
            code=745525,
            secret='ABCDEF',
            query='a=1&b=2',
            path='/apiv1/devices/SM-12345678'
        )

        when(
            'Trying invalid code',
            form=dict(
                activationCode=['badCode']
            )
        )

        assert response.status == 400


def test_path_parameters_encoding():
    def app(environ, start_response):
        start_response('200 OK', [
            ('Content-Type', 'text/plain'),
        ])
        path = environ.get('PATH_INFO')
        return [path]

    with Given(app, '/id: foo%20bar'):
        assert response.status == 200
        assert response == '/foo bar'

        when(path_parameters=given | dict(id='foo Bar'))
        assert response.status == 200
        assert response == '/foo Bar'


def test_path_parameters():
    call = dict(
        title='Multiple path parameters',
        path='/apiv1/devices/name: SM 12345678/id: 1',
        verb='POST',
        form=dict(
            activationCode=['746727'],
            phone=['+9897654321']
        ),
    )

    with Given(wsgi_application, **call):
        assert response.status == '200 OK'
        assert response.json == {
            'code': 745525,
            'query': None,
            'secret': 'ABCDEF',
            'path': '/apiv1/devices/SM 12345678/1',
        }

        when(path_parameters=given | dict(name='foo'))
        assert response.status == '200 OK'
        assert response.json == {
            'code': 745525,
            'query': None,
            'secret': 'ABCDEF',
            'path': '/apiv1/devices/foo/1',
        }

        with pytest.raises(InvalidUrlParametersError):
            when(
                title='Incomplete path parameters',
                path_parameters=dict(
                    id=2
                )
            )

        with pytest.raises(InvalidUrlParametersError):
            when(
                title='Extra path parameters',
                path_parameters=dict(
                    name='any',
                    id=3,
                    garbage='yes'
                )
            )

        with pytest.raises(InvalidUrlParametersError):
            when(
                title='Without path parameters',
                path_parameters=None
            )

    call = dict(
        title='No path parameters',
        path='/apiv1/devices',
        verb='POST',
        form=dict(
            activationCode=['746727'],
            phone=['+9897654321']
        ),
    )

    with Given(wsgi_application, **call):
        assert response.status == '200 OK'


def test_to_dict():
    call = dict(
        title='Binding',
        description='Awesome given description',
        path='/apiv1/devices/name: SM-12345678',
        verb='POST',
        as_='visitor',
        form=dict(
            activationCode=['746727'],
            phone=['+9897654321']
        ),
        headers=[('X-H1', 'Header Value')]
    )
    with Given(wsgi_application, **call):
        assert response.status == '200 OK'
        when(
            title='Trying invalid code',
            description='Awesome invalid code description',
            form=dict(
                activationCode=['badCode']
            )
        )
        assert response.status == 400

        story_dict = story.to_dict()
        assert story_dict['base_call'] == dict(
            title='Binding',
            description='Awesome given description',
            path='/apiv1/devices/:name',
            verb='POST',
            as_='visitor',
            path_parameters=dict(name='SM-12345678'),
            form=dict(
                activationCode=['746727'],
                phone=['+9897654321']
            ),
            headers=[
                'X-H1: Header Value',
            ],
            response=dict(
                status='200 OK',
                headers=[
                    'Content-Type: application/json;charset=utf-8',
                    'X-Pagination-Count: 10'
                ],
                json={
                    'secret': 'ABCDEF',
                    'code': 745525,
                    'query': None,
                    'path': '/apiv1/devices/SM-12345678'
                }
            )
        )
        assert story_dict['calls'][0] == dict(
            title='Trying invalid code',
            description='Awesome invalid code description',
            form=dict(
                activationCode=['badCode']
            ),
            response=dict(
                headers=['Content-Type: text/plain;utf-8'],
                status='400 Bad Request',
            )
        )


def test_from_dict():
    data = dict(
        base_call=dict(
            title='Binding',
            path='/apiv1/devices/:name',
            verb='POST',
            as_='visitor',
            path_parameters=dict(name='SM-12345678'),
            form=dict(
                activationCode=['746727'],
                phone=['+9897654321']
            ),
            headers=['X-H1: Header Value'],
            response=dict(
                status='200 OK',
                headers=[
                    'Content-Type: application/json;charset=utf-8',
                    'X-Pagination-Count: 10'
                ],
                json={'secret': 'ABCDEF', 'code': 745525, 'query': ''}
            )
        ),
        calls=[
            dict(
                title='Trying invalid code',
                form=dict(
                    activationCode=['badCode']
                ),
                response=dict(
                    headers=['Content-Type: text/plain;utf-8'],
                    status='400 Bad Request',
                )
            )
        ]
    )
    loaded_story = Story.from_dict(data)
    assert loaded_story is not None
    assert isinstance(loaded_story.base_call, Call)
    assert isinstance(loaded_story.calls[0], AlteredCall)
    assert loaded_story.base_call.response.status == 200
    assert data == loaded_story.to_dict()


def test_dump_load():
    call = dict(
        title='Binding',
        path='/apiv1/devices/name: SM-12345678',
        verb='POST',
        as_='visitor',
        form=dict(
            activationCode=['746727'],
            phone='+9897654321'
        ),
        headers=[('X-H1', 'Header Value')]
    )
    with Given(wsgi_application, **call):
        assert response.status == '200 OK'
        when(
            'Trying invalid code',
            form=dict(
                activationCode=['badCode']
            )
        )
        assert response.status == 400

        dumped_story = story.dumps()
        loaded_story = Story.loads(dumped_story)
        assert story.to_dict() == loaded_story.to_dict()
        loaded_story.validate()


def test_verify():
    call = dict(
        title='Binding',
        path='/apiv1/devices/name: SM-12345678',
        verb='POST',
        as_='visitor',
        form=dict(
            activationCode=['746727'],
            phone='+9897654321'
        ),
        headers=[('X-H1', 'Header Value')]
    )
    with Given(wsgi_application, **call):
        assert response.status == '200 OK'
        when(
            'Trying invalid code',
            form=dict(
                activationCode=['badCode']
            )
        )
        dumped_story = story.dumps()

    loaded_story = Story.loads(dumped_story)
    loaded_story.verify(wsgi_application)

    loaded_story.base_call.response.body = '{"a": 1}'

    with pytest.raises(CallVerifyError):
        loaded_story.verify(wsgi_application)


def test_dump_load_file():
    with tempfile.TemporaryFile(mode='w+', encoding='utf-8') as temp_file:
        call = dict(
            title='Binding',
            path='/apiv1/devices/name: SM-12345678',
            verb='POST',
            as_='visitor',
            form=dict(
                activationCode=['746727'],
                phone=['+9897654321']
            ),
            headers=[('X-H1', 'Header Value')]
        )
        with Given(wsgi_application, **call):
            assert response.status == '200 OK'
            when(
                'Trying invalid code',
                form=dict(
                    activationCode=['badCode']
                )
            )
            story.dump(temp_file)

        temp_file.seek(0)
        loaded_story = Story.load(temp_file)
        assert loaded_story.verify(wsgi_application) is None


def test_path_overriding():
    call = dict(
        title='Multiple path parameters',
        path='/apiv1/devices/name: SM-12345678/id: 1',
        verb='POST',
        form=dict(
            activationCode='746727',
            phone=['+9897654321']
        ),
    )

    with Given(wsgi_application, **call):
        assert response.status == '200 OK'

        modified_call = when(
            path='/apiv1/devices?a=b&c=d'
        )
        assert modified_call.path_parameters is None
        assert response.status == 200
        assert response.json['query'] == 'a=b&c=d'


def test_authorization():
    def wsgi_application(environ, start_response):
        result = {}
        identity = environ.get('HTTP_AUTHORIZATION')
        if identity:
            result['identity'] = identity
        start_response('200 OK', [
            ('Content-Type', 'application/json;charset=utf-8'),
        ])

        yield json.dumps(result).encode()

    with Given(
        wsgi_application, title='Testing authorization header',
        path='/',
        authorization='testuser'
    ):
        assert response.json['identity'] == 'testuser'
