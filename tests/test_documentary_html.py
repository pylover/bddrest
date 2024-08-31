import io

from bddrest import Story


def test_html():

    def get_field_info(call):
        return dict(), dict(
            f1=dict(required=True, not_none=True, type='str'),
        )

    story = Story.loads(provided_story)
    outfile = io.StringIO()
    story.document(
        onfile=lambda _: outfile,
        onstory=get_field_info,
        format='html'
    )
    outputstring = outfile.getvalue()
    assert expected_html == outputstring


provided_story = '''
    base_call:
      as_: visitor
      title: Quickstart!
      description: Awesome API!
      path: /books/:id
      path_parameters:
        id: '1'
      query:
        a: 1
        b: '2'
      verb: PUT
      form:
        f1: abc
        f2: 123
      headers:
        - 'Content-Type: application/json;charset=utf-8'
      response:
        headers:
        - 'Content-Type: application/json;charset=utf-8'
        json:
          foo: bar
        status: 200 OK
    calls:
    - response:
        headers:
        - 'Content-Type: text/plain;charset=utf-8'
        status: 404 Not Found
      title: Trying invalid book id
      description: trying an invalid book id.
      path_parameters:
        id: None
      query:
        a: 2
        b: 4
      headers:
      - 'A: B'
      form:
        f1: cba
'''


expected_html = '''\
<h2>
Quickstart!
</h2>
<h3>
PUT /books/:id
</h3>
<p>
Awesome API!
</p>
<h3>
Path Parameters
</h3>
<table>
<tr>
<th>
Name
</th>
<th>
Example
</th>
</tr>
<tr>
<td>
id
</td>
<td>
1
</td>
</tr>
</table>
<h3>
Query Strings
</h3>
<table>
<tr>
<th>
Name
</th>
<th>
Example
</th>
</tr>
<tr>
<td>
a
</td>
<td>
1
</td>
</tr>
<tr>
<td>
b
</td>
<td>
2
</td>
</tr>
</table>
<h3>
Form
</h3>
<table>
<tr>
<th>
Name
</th>
<th>
Required
</th>
<th>
Type
</th>
<th>
Example
</th>
</tr>
<tr>
<td>
f1
</td>
<td>
Yes
</td>
<td>
str
</td>
<td>
abc
</td>
</tr>
<tr>
<td>
f2
</td>
<td>
?
</td>
<td>
?
</td>
<td>
123
</td>
</tr>
</table>
<h3>
Request Headers
</h3>
<ul>
<li>
Content-Type: application/json;charset=utf-8
</li>
</ul>
<h3>
CURL
</h3>
<pre>
<code>
curl -X PUT -F "f1=abc" -F "f2=123" -H "Content-Type: application/json;charset=utf-8" -- "$URL/books/1?a=1&b=2"
</code>
</pre>
<h3>
Response: 200 OK
</h3>
<h4>
Body
</h4>
<p>
Content-Type: application/json
</p>
<pre>
<code>
{"foo": "bar"}
</code>
</pre>
<hr/>
<h2>
WHEN: Trying invalid book id
</h2>
<h3>
PUT /books/:id
</h3>
<p>
trying an invalid book id.
</p>
<h3>
Path Parameters
</h3>
<table>
<tr>
<th>
Name
</th>
<th>
Example
</th>
</tr>
<tr>
<td>
id
</td>
<td>
None
</td>
</tr>
</table>
<h3>
Query Strings
</h3>
<table>
<tr>
<th>
Name
</th>
<th>
Example
</th>
</tr>
<tr>
<td>
a
</td>
<td>
2
</td>
</tr>
<tr>
<td>
b
</td>
<td>
4
</td>
</tr>
</table>
<h3>
Form
</h3>
<table>
<tr>
<th>
Name
</th>
<th>
Required
</th>
<th>
Type
</th>
<th>
Example
</th>
</tr>
<tr>
<td>
f1
</td>
<td>
Yes
</td>
<td>
str
</td>
<td>
cba
</td>
</tr>
</table>
<h3>
Request Headers
</h3>
<ul>
<li>
A: B
</li>
</ul>
<h3>
CURL
</h3>
<pre>
<code>
curl -X PUT -F "f1=cba" -H "A: B" -- "$URL/books/None?a=2&b=4"
</code>
</pre>
<h3>
Response: 404 Not Found
</h3>
'''  # noqa
