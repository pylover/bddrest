import cgi
import json
import tempfile

import pytest

from bddrest import Given, when, story, response, InvalidUrlParametersError, \
    CallVerifyError, Call, AlteredCall, Story


def wsgi_application(environ, start_response):
    form = cgi.FieldStorage(
        fp=environ['wsgi.input'],
        environ=environ,
        strict_parsing=False,
        keep_blank_values=True
    )

    try:
        # FIXME: Why x ^ 1234
        code = int(form['activationCode'].value) ^ 1234
    except ValueError:
        start_response('400 Bad Request', [('Content-Type', 'text/plain;utf-8')])
        return

    start_response('200 OK', [
        ('Content-Type', 'application/json;charset=utf-8'),
        ('X-Pagination-Count', '10')
    ])
    result = dict(
        secret='ABCDEF',
        code=code,
        query=environ['QUERY_STRING'],
    )

    identity = environ.get('HTTP_AUTHORIZATION')
    if identity:
        result['identity'] = identity
    yield json.dumps(result).encode()


def test_given_when():
    call = dict(
        title='Binding and registering the device after verifying the activation code',
        description=\
            'As a new visitor I have to bind my device with activation code and phone number',
        url='/apiv1/devices/name: SM-12345678',
        verb='POST',
        as_='visitor',
        query=dict(
            a=1,
            b=2
        ),
        form=dict(
            activationCode='746727',
            phone='+9897654321'
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
        assert response.json ==  dict(
            code=745525,
            secret='ABCDEF',
            query='a=1&b=2'
        )

        when(
            'Trying invalid code',
            form=dict(
                activationCode='badCode'
            )
        )

        assert response.status == 400


def test_url_parameters():
    call = dict(
        title='Multiple url parameters',
        url='/apiv1/devices/name: SM-12345678/id: 1',
        verb='POST',
        form=dict(
            activationCode='746727',
            phone='+9897654321'
        ),
    )

    with Given(wsgi_application, **call):
        assert response.status == '200 OK'

        with pytest.raises(InvalidUrlParametersError):
            when(
                title='Incomplete url parameters',
                url_parameters=dict(
                    id=2
                )
            )

        with pytest.raises(InvalidUrlParametersError):
            when(
                title='Extra url parameters',
                url_parameters=dict(
                    name='any',
                    id=3,
                    garbage='yes'
                )
            )

        with pytest.raises(InvalidUrlParametersError):
            when(
                title='Without url parameters',
                url_parameters=None
            )

    call = dict(
        title='No url parameters',
        url='/apiv1/devices',
        verb='POST',
        form=dict(
            activationCode='746727',
            phone='+9897654321'
        ),
    )

    with Given(wsgi_application, **call):
        assert response.status == '200 OK'

def test_to_dict():
    call = dict(
        title='Binding',
        description='Awesome given description',
        url='/apiv1/devices/name: SM-12345678',
        verb='POST',
        as_='visitor',
        form=dict(
            activationCode='746727',
            phone='+9897654321'
        ),
        headers=[('X-H1', 'Header Value')]
    )
    with Given(wsgi_application, **call):
        assert response.status == '200 OK'
        when(
            'Trying invalid code',
            description='Awesome invalid code description',
            form=dict(
                activationCode='badCode'
            )
        )
        assert response.status == 400

        story_dict = story.to_dict()
        assert story_dict['base_call'] == dict(
            title='Binding',
            description='Awesome given description',
            url='/apiv1/devices/:name',
            verb='POST',
            as_='visitor',
            url_parameters=dict(name='SM-12345678'),
            form=dict(
                activationCode='746727',
                phone='+9897654321'
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
        )
        assert story_dict['calls'][0] == dict(
            title='Trying invalid code',
            description='Awesome invalid code description',
            form=dict(
                activationCode='badCode'
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
            url='/apiv1/devices/:name',
            verb='POST',
            as_='visitor',
            url_parameters=dict(name='SM-12345678'),
            form=dict(
                activationCode='746727',
                phone='+9897654321'
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
                    activationCode='badCode'
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
        url='/apiv1/devices/name: SM-12345678',
        verb='POST',
        as_='visitor',
        form=dict(
            activationCode='746727',
            phone='+9897654321'
        ),
        headers=[('X-H1', 'Header Value')]
    )
    with Given(wsgi_application, **call):
        assert response.status == '200 OK'
        when(
            'Trying invalid code',
            form=dict(
                activationCode='badCode'
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
        url='/apiv1/devices/name: SM-12345678',
        verb='POST',
        as_='visitor',
        form=dict(
            activationCode='746727',
            phone='+9897654321'
        ),
        headers=[('X-H1', 'Header Value')]
    )
    with Given(wsgi_application, **call):
        assert response.status == '200 OK'
        when(
            'Trying invalid code',
            form=dict(
                activationCode='badCode'
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
            url='/apiv1/devices/name: SM-12345678',
            verb='POST',
            as_='visitor',
            form=dict(
                activationCode='746727',
                phone='+9897654321'
            ),
            headers=[('X-H1', 'Header Value')]
        )
        with Given(wsgi_application, **call):
            assert response.status == '200 OK'
            when(
                'Trying invalid code',
                form=dict(
                    activationCode='badCode'
                )
            )
            story.dump(temp_file)

        temp_file.seek(0)
        loaded_story = Story.load(temp_file)
        assert loaded_story.verify(wsgi_application) is None


def test_url_overriding():
    call = dict(
        title='Multiple url parameters',
        url='/apiv1/devices/name: SM-12345678/id: 1',
        verb='POST',
        form=dict(
            activationCode='746727',
            phone='+9897654321'
        ),
    )

    with Given(wsgi_application, **call):
        assert response.status == '200 OK'

        modified_call = when(
            'Trying different url!',
            url='/apiv1/devices?a=b&c=d'
        )
        assert modified_call.url_parameters is None
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
        url='/',
        authorization='testuser'
    ):
        assert response.json['identity'] == 'testuser'

