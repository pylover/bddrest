import cgi
import functools
import json
import tempfile
import unittest

from bddrest.authoring import given, when, then, composer, response, and_
from bddrest.exceptions import InvalidUrlParametersError, CallVerifyError
from bddrest.specification import Call, When
from bddrest.story import Story


def wsgi_application(environ, start_response):
    form = cgi.FieldStorage(
        fp=environ['wsgi.input'],
        environ=environ,
        strict_parsing=False,
        keep_blank_values=True
    )

    try:
        code = int(form['activationCode'].value) ^ 1234
    except ValueError:
        start_response('400 Bad Request', [('Content-Type', 'text/plain;utf-8')])
        return

    start_response('200 OK', [
        ('Content-Type', 'application/json;charset=utf-8'),
        ('X-Pagination-Count', '10')
    ])
    result = json.dumps(dict(
        secret='ABCDEF',
        code=code,
        query=environ['QUERY_STRING']
    ))
    yield result.encode()


class StoryTestCase(unittest.TestCase):

    def test_given_when_then(self):
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
        with given(wsgi_application, **call):
            then(
                response.status == '200 OK',
                response.status_code == 200
            )
            and_('secret' in response.json)
            and_(response.json['secret'] == 'ABCDEF')
            and_('Bad Header' not in response.headers)
            # and_(response.headers.get('X-Pagination-Count') == '10')
            and_(response.content_type == 'application/json')
            and_(self.assertDictEqual(response.json, dict(
                code=745525,
                secret='ABCDEF',
                query='a=1&b=2'
            )))

            when(
                'Trying invalid code',
                form=dict(
                    activationCode='badCode'
                )
            )

            then(response.status_code == 400)

    def test_url_parameters(self):
        call = dict(
            title='Multiple url parameters',
            url='/apiv1/devices/name: SM-12345678/id: 1',
            verb='POST',
            form=dict(
                activationCode='746727',
                phone='+9897654321'
            ),
        )

        with given(wsgi_application, **call):
            then(response.status == '200 OK')

            with self.assertRaises(InvalidUrlParametersError):
                when(
                    title='Incomplete url parameters',
                    url_parameters=dict(
                        id=2
                    )
                )

            with self.assertRaises(InvalidUrlParametersError):
                when(
                    title='Extra url parameters',
                    url_parameters=dict(
                        name='any',
                        id=3,
                        garbage='yes'
                    )
                )

            with self.assertRaises(InvalidUrlParametersError):
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

        with given(wsgi_application, **call):
            then(response.status == '200 OK')

    def test_to_dict(self):
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
        with given(wsgi_application, **call):
            then(response.status == '200 OK')
            when(
                'Trying invalid code',
                description='Awesome invalid code description',
                form=dict(
                    activationCode='badCode'
                )
            )
            then(response.status_code == 400)

            story_dict = composer.to_dict()
            self.assertDictEqual(story_dict['base_call'], dict(
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
            ))
            self.assertDictEqual(story_dict['calls'][0], dict(
                title='Trying invalid code',
                description='Awesome invalid code description',
                form=dict(
                    activationCode='badCode'
                ),
                response=dict(
                    headers=['Content-Type: text/plain;utf-8'],
                    status='400 Bad Request',
                )
            ))

    def test_from_dict(self):
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
        self.assertIsNotNone(loaded_story)
        self.assertIsInstance(loaded_story.base_call, Call)
        self.assertIsInstance(loaded_story.calls[0], When)

        self.assertEqual(loaded_story.base_call.response.status_code, 200)
        self.maxDiff = None
        self.assertDictEqual(data, loaded_story.to_dict())

    def test_dump_load(self):
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
        with given(wsgi_application, **call):
            then(response.status == '200 OK')
            when(
                'Trying invalid code',
                form=dict(
                    activationCode='badCode'
                )
            )
            then(response.status_code == 400)

            dumped_story = composer.dumps()
            loaded_story = Story.loads(dumped_story)
            self.assertDictEqual(composer.to_dict(), loaded_story.to_dict())
            loaded_story.validate()

    def test_verify(self):
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
        with given(wsgi_application, **call):
            then(response.status == '200 OK')
            when(
                'Trying invalid code',
                form=dict(
                    activationCode='badCode'
                )
            )
            dumped_story = composer.dumps()

        loaded_story = Story.loads(dumped_story)
        loaded_story.verify(wsgi_application)

        loaded_story.base_call.response.body = '{"a": 1}'
        self.assertRaises(
            CallVerifyError,
            functools.partial(loaded_story.verify, wsgi_application)
        )

    def test_dump_load_file(self):
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
            with given(wsgi_application, **call):
                then(response.status == '200 OK')
                when(
                    'Trying invalid code',
                    form=dict(
                        activationCode='badCode'
                    )
                )
                composer.dump(temp_file)

            temp_file.seek(0)
            loaded_story = Story.load(temp_file)
            self.assertIsNone(loaded_story.verify(wsgi_application))

    def test_url_overriding(self):
        call = dict(
            title='Multiple url parameters',
            url='/apiv1/devices/name: SM-12345678/id: 1',
            verb='POST',
            form=dict(
                activationCode='746727',
                phone='+9897654321'
            ),
        )

        with given(wsgi_application, **call):
            then(response.status == '200 OK')

            modified_call = when(
                'Trying different url!',
                url='/apiv1/devices?a=b&c=d'
            )
            self.assertIsNone(modified_call.url_parameters)

            then(
                response.status_code == 200,
                response.json['query'] == 'a=b&c=d'
            )


if __name__ == '__main__':  # pragma: no cover
    unittest.main()

