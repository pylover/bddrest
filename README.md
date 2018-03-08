# bddrest

Toolchain to define and verify REST API in BDD.

[![Build Status](http://img.shields.io/pypi/v/bddrest.svg)](https://pypi.python.org/pypi/bddrest)
     
## Branches

### master

[![Build Status](https://travis-ci.org/Carrene/bddrest.svg?branch=master)](https://travis-ci.org/Carrene/bddrest)
[![Coverage Status](https://coveralls.io/repos/github/Carrene/bddrest/badge.svg?branch=master)](https://coveralls.io/github/Carrene/bddrest?branch=master)

### develop

[![Build Status](https://travis-ci.org/Carrene/bddrest.svg?branch=develop)](https://travis-ci.org/Carrene/bddrest)
[![Coverage Status](https://coveralls.io/repos/github/Carrene/bddrest/badge.svg?branch=develop)](https://coveralls.io/github/Carrene/bddrest?branch=develop)


## Quick start

### Writing tests

```python

import sys
import json

from bddrest.authoring import given, when, then, and_, response, composer


def wsgi_application(environ, start_response):
    path = environ['PATH_INFO']
    if path.endswith('/None'):
        start_response('404 Not Found', [('Content-Type', 'text/plain;charset=utf-8')])
        return ''
    start_response('200 OK', [('Content-Type', 'application/json;charset=utf-8')])
    result = json.dumps(dict(
        foo='bar'
    ))
    yield result.encode()


with given(
        wsgi_application,
        title='Quickstart!',
        url='/books/id: 1',
        as_='visitor'):

    then(response.status == '200 OK')
    and_('foo' in response.json)
    and_(response.json['foo'] == 'bar')

    when(
        'Trying invalid book id',
        url_parameters={'id': None}
    )

    then(response.status_code == 404)

    composer.dump(sys.stdout)

```

Will produce:

```yaml

base_call:
  as_: visitor
  response:
    headers:
    - 'Content-Type: application/json;charset=utf-8'
    json:
      foo: bar
    status: 200 OK
  title: Quickstart!
  url: /books/:id
  url_parameters:
    id: '1'
  verb: GET
calls:
- response:
    headers:
    - 'Content-Type: text/plain;charset=utf-8'
    status: 404 Not Found
  title: Trying invalid book id
  url_parameters:
    id: None

```

