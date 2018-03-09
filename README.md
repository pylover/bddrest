# bddrest

Toolchain to define and verify REST API in BDD.

[![Build Status](http://img.shields.io/pypi/v/bddrest.svg)](https://pypi.python.org/pypi/bddrest)

Table of Contents
=================

   * [bddrest](#bddrest)
      * [Branches](#branches)
         * [master](#master)
         * [develop](#develop)
      * [Quick start](#quick-start)
         * [Writing tests](#writing-tests)
         * [Dumping a Story](#dumping-a-story)
         * [Markdown](#markdown)


     
## Branches

### master

[![Build Status](https://travis-ci.org/Carrene/bddrest.svg?branch=master)](https://travis-ci.org/Carrene/bddrest)
[![Coverage Status](https://coveralls.io/repos/github/Carrene/bddrest/badge.svg?branch=master)](https://coveralls.io/github/Carrene/bddrest?branch=master)

### develop

[![Build Status](https://travis-ci.org/Carrene/bddrest.svg?branch=develop)](https://travis-ci.org/Carrene/bddrest)
[![Coverage Status](https://coveralls.io/repos/github/Carrene/bddrest/badge.svg?branch=develop)](https://coveralls.io/github/Carrene/bddrest?branch=develop)


## Quick start

### Writing tests

Using `given`, `when`, `then` and `and_` functions as you see in the example below, you can determine and assert 
the behaviour of yout `REST API`.

The `composer` and `response` objects are two proxies for currently writing story(*inside the with given( ... ): context*) 
and the last response after a `given` and or `when`.

```python

import sys
import json

from bddrest.authoring import given, when, then, and_, response, composer


def wsgi_application(environ, start_response):
    path = environ['PATH_INFO']
    if path.endswith('/None'):
        start_response('404 Not Found', [('Content-Type', 'text/plain;charset=utf-8')])
        yield b''
    else:
        start_response('200 OK', [('Content-Type', 'application/json;charset=utf-8')])
        result = json.dumps(dict(
            foo='bar'
        ))
        yield result.encode()


with given(
        wsgi_application,
        title='Quickstart!',
        url='/books/id: 1',
        as_='visitor') as story:

    then(response.status == '200 OK')
    and_('foo' in response.json)
    and_(response.json['foo'] == 'bar')

    when(
        'Trying invalid book id',
        url_parameters={'id': None}
    )

    then(response.status_code == 404)

```

### Dumping a `Story`

```python
story.dumps()
```

Produces:

```yaml
base_call:
  as_: visitor
  description: As a member I have to POST a book to the library.
  form:
    name: BDD Book
  query:
    a: b
  response:
    headers:
    - 'Content-Type: application/json;charset=utf-8'
    json:
      foo: bar
    status: 200 OK
  title: Posting a book
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

You may load the story again from this yaml with `Story.loads(yaml)`.

There is two additional methods are available to dump and load to 
and from a file: `story.load(file)` and `story.dump(file)`

### Markdown

You can use `story.document([formatter_factory=MarkdownFormatter])` to generate documentation 
in arbitrary format for example: `Markdown`.


    ## Posting a book
    
    ### GET /books/:id
    
    As a member I have to POST a book to the library.
    
    ### Url Parameters
    
    Name | Example
    --- | ---
    id | 1
    
    ### Query Strings
    
    Name | Example
    --- | ---
    a | b
    
    ### Form
    
    Name | Example
    --- | ---
    name | BDD Book
    
    ### Response: 200 OK
    
    #### Headers
    
    * Content-Type: application/json;charset=utf-8
    
    #### Body
    
    ```json
    {"foo": "bar"}
    ```
    
    ## WHEN: Trying invalid book id
    
    ### Url Parameters
    
    Name | Example
    --- | ---
    id | None
    
    ### Response: 404 Not Found
    
    #### Headers
    
    * Content-Type: text/plain;charset=utf-8


Which renders as:

## Posting a book

### GET /books/:id

As a member I have to POST a book to the library.

### Url Parameters

Name | Example
--- | ---
id | 1

### Query Strings

Name | Example
--- | ---
a | b

### Form

Name | Example
--- | ---
name | BDD Book

### Response: 200 OK

#### Headers

* Content-Type: application/json;charset=utf-8

#### Body

```json
{"foo": "bar"}
```

## WHEN: Trying invalid book id

### Url Parameters

Name | Example
--- | ---
id | None

### Response: 404 Not Found

#### Headers

* Content-Type: text/plain;charset=utf-8

