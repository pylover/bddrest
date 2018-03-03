# bddrest

Toolchain to define and verify REST API in BDD.

[![Build Status](http://img.shields.io/pypi/v/bddrest.svg)](https://pypi.python.org/pypi/bddrest)
[![Gitter](https://img.shields.io/gitter/room/Carrene/bddrest.svg)](https://gitter.im/Carrene/bddrest)
     
## Branches

### master

[![Build Status](https://travis-ci.org/Carrene/bddrest.svg?branch=master)](https://travis-ci.org/Carrene/bddrest)
[![Coverage Status](https://coveralls.io/repos/github/Carrene/bddrest/badge.svg?branch=master)](https://coveralls.io/github/Carrene/bddrest?branch=master)

### develop

[![Build Status](https://travis-ci.org/Carrene/bddrest.svg?branch=develop)](https://travis-ci.org/Carrene/bddrest)
[![Coverage Status](https://coveralls.io/repos/github/Carrene/bddrest/badge.svg?branch=develop)](https://coveralls.io/github/Carrene/bddrest?branch=develop)


## Quick start


```python

from bddrest import given, when, then, and_, response


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


```
