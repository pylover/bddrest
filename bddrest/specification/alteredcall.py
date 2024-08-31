from .call import Call
from ..helpers import querystring_parse
from ..headerset import HeaderSet


class Unchanged:
    pass


UNCHANGED = Unchanged()


class AlteredCall(Call):
    def __init__(self, base_call, path=UNCHANGED, verb=UNCHANGED,
                 path_parameters=UNCHANGED, form=UNCHANGED, json=UNCHANGED,
                 multipart=UNCHANGED, content_type=UNCHANGED,
                 headers=UNCHANGED, as_=UNCHANGED, query=UNCHANGED, title=None,
                 description=None, extra_environ=UNCHANGED,
                 response=None, authorization=UNCHANGED,
                 body=UNCHANGED, https=UNCHANGED):
        self.base_call = base_call
        self.diff = {}
        super().__init__(
            title=title,
            description=description,
            response=response
        )

        self.path = path
        if path_parameters is not UNCHANGED:
            self.path_parameters = path_parameters

        if query is not UNCHANGED:
            self.query = query

        self.extra_environ = extra_environ
        self.verb = verb
        if body is not UNCHANGED:
            self.body = body
            self.form = None
            self.json = None
            self.multipart = None
        else:
            self.form = form
            self.json = json
            self.multipart = multipart

        self.content_type = content_type
        self.authorization = authorization
        self.headers = headers
        self.as_ = as_
        self.https = https

    def to_dict(self):
        result = dict(title=self.title)
        result.update(self.diff)

        if self.description is not None:
            result['description'] = self.description

        if self.response is not None:
            result['response'] = self.response.to_dict()

        return result

    def update_diff(self, key, value):
        if value is UNCHANGED:
            self.diff.pop(key, None)
            return

        self.diff[key] = value

    @property
    def path(self):
        return self.diff.get('path', self.base_call.path)

    @path.setter
    def path(self, value):
        if value is UNCHANGED:
            self.diff.pop('path', None)
            return

        path, path_parameters, query = self.extract_path_parameters(value)
        if path and path != self.base_call.path:
            self.diff['path'] = path
            self.path_parameters = path_parameters
            self.query = query

    @property
    def path_parameters(self):
        return self.diff.get('path_parameters', self.base_call.path_parameters)

    @path_parameters.setter
    def path_parameters(self, value):
        self.update_diff('path_parameters', value)

    @path_parameters.deleter
    def path_parameters(self):
        del self.diff['path_parameters']

    @property
    def verb(self):
        return self.diff.get('verb', self.base_call.verb)

    @verb.setter
    def verb(self, value):
        self.update_diff('verb', value)

    @verb.deleter
    def verb(self):
        del self.diff['verb']

    @property
    def headers(self):
        return self.diff.get('headers', self.base_call.headers)

    @headers.setter
    def headers(self, value):
        self.update_diff(
            'headers',
            value if value is UNCHANGED else HeaderSet(value)
        )

    @headers.deleter
    def headers(self):
        del self.diff['headers']

    @property
    def query(self):
        return self.diff.get('query', self.base_call.query)

    @query.setter
    def query(self, value):
        self.update_diff(
            'query',
            value if value is UNCHANGED else querystring_parse(value)
        )

    @query.deleter
    def query(self):
        del self.diff['query']

    @property
    def content_type(self):
        return self.diff.get('content_type', self.base_call.content_type)

    @content_type.setter
    def content_type(self, value):
        self.update_diff('content_type', value)

    @content_type.deleter
    def content_type(self):
        del self.diff['content_type']

    @property
    def authorization(self):
        return self.diff.get('authorization', self.base_call.authorization)

    @authorization.setter
    def authorization(self, value):
        self.update_diff('authorization', value)

    @authorization.deleter
    def authorization(self):
        del self.diff['authorization']

    @property
    def as_(self):
        return self.diff.get('as_', self.base_call.as_)

    @as_.setter
    def as_(self, value):
        self.update_diff('as_', value)

    @as_.deleter
    def as_(self):
        del self.diff['as_']

    @property
    def extra_environ(self):
        return self.diff.get('extra_environ', self.base_call.extra_environ)

    @extra_environ.setter
    def extra_environ(self, value):
        self.update_diff('extra_environ', value)

    @extra_environ.deleter
    def extra_environ(self):
        del self.diff['extra_environ']

    @property
    def body(self):
        return self.diff.get('body', self.base_call.body)

    @body.setter
    def body(self, value):
        self.update_diff('body', value)

    @body.deleter
    def body(self):
        del self.diff['body']

    @property
    def form(self):
        return self.diff.get('form', self.base_call.form)

    @form.setter
    def form(self, value):
        self.update_diff(
            'form',
            value if value is UNCHANGED else querystring_parse(value)
        )

    @form.deleter
    def form(self):
        del self.diff['form']

    @property
    def json(self):
        return self.diff.get('json', self.base_call.json)

    @json.setter
    def json(self, value):
        self.update_diff('json', value)

    @json.deleter
    def json(self):
        del self.diff['json']

    @property
    def multipart(self):
        return self.diff.get('multipart', self.base_call.multipart)

    @multipart.setter
    def multipart(self, value):
        self.update_diff('multipart', value)

    @multipart.deleter
    def multipart(self):
        del self.diff['multipart']

    @property
    def https(self):
        return self.diff.get('https', self.base_call.https)

    @https.setter
    def https(self, value):
        self.update_diff('https', value)
