import cgi
import json
import pytest

from bddrest import Given, Append, Remove, Update, when, response, given_form


def wsgi_application(environ, start_response):
    form = cgi.FieldStorage(
        fp=environ['wsgi.input'],
        environ=environ,
        strict_parsing=False,
        keep_blank_values=True
    )

    start_response('200 OK', [
        ('Content-Type', 'application/json;charset=utf-8'),
    ])
    yield json.dumps({k: form[k].value for k in form.keys()}).encode()


def test_append_form_field():
    call = dict(
        title='test add form field',
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
            'Adding another field',
            form=Append(email='user@example.com')
        )
        assert response.json == dict(
            activationCode='746727',
            phone='+9897654321',
            email='user@example.com'
        )


def test_remove_from_fields():
    call = dict(
        title='test remove form fields',
        url='/apiv1/devices/name: SM-12345678/id: 1',
        verb='POST',
        form=dict(
            activationCode='746727',
            phone='+9897654321',
            email='user@example.com'
        )
    )

    with Given(wsgi_application, **call):
        assert response.status =='200 OK'

        when('Removing fields', form=Remove('email', 'phone'))
        assert response.json == dict(activationCode='746727')

        with pytest.raises(ValueError):
            Remove('a').apply(['b', 'c'])

        with pytest.raises(ValueError):
            Remove('a').apply({'b': 'c'})


def test_update_from_fields():
    call = dict(
        title='test remove form fields',
        url='/apiv1/devices/name: SM-12345678/id: 1',
        verb='POST',
        form=dict(
            activationCode='746727',
            email='user@example.com'
        )
    )

    with Given(wsgi_application, **call):
        assert response.status =='200 OK'
        assert response.json == dict(
            activationCode='746727',
            email='user@example.com'
        )


        when(
            'Updating email and phone fields',
            form=Update(email='test@example.com', phone='+98123456789')
        )
        assert response.json == dict(
            activationCode='746727',
            phone='+98123456789',
            email='test@example.com'
        )

        when(
            'Updating only acitvation code',
            form=Update(activationCode='666')
        )
        assert response.json == dict(
            activationCode='666',
            email='user@example.com'
        )

        when('Not updating at all')
        assert response.json == dict(
            activationCode='746727',
            email='user@example.com'
        )


def test_form_operators():
    call = dict(
        title='test form fields operators: + and -',
        verb='POST',
        form=dict(
            a='1',
            b='2'
        )
    )

    with Given(wsgi_application, **call):
        assert response.status =='200 OK'
        assert response.json == dict(
            a='1',
            b='2'
        )

        when('Removing an item', form=given_form - 'a')
        assert response.json == dict(
            b='2'
        )

        when('Removing multiple items', form=given_form - ['a', 'b'])
        assert response.json == dict()

        when('Appending an item', form=given_form + dict(c=3))
        assert response.json == dict(
            a='1',
            b='2',
            c='3'
        )

        when('Updating some items', form=given_form | dict(c=3, b=4))
        assert response.json == dict(
            a='1',
            b='4',
            c='3',
        )

        when(
            'Combining with the other manipulation types',
            form=Append(d=4) - 'b' + dict(c=3) | dict(z=1, a=2)
        )
        assert response.json == dict(
            a='2',
            c='3',
            d='4',
            z='1',
        )

        when(
            'Remove an item with more than one character',
            form=given_form + dict(word='alphabet') - 'word'
        )
        assert response.json == dict(
            a='1',
            b='2',
        )
