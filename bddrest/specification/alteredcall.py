from ..helpers import normalize_query_string
from .call import Call
from .headerset import HeaderSet
from .response import Response


class Unchanged:
    pass


UNCHANGED = Unchanged()


class AlteredCall(Call):
    def __init__(self, base_call, title, url=UNCHANGED, verb=UNCHANGED,
                 url_parameters=UNCHANGED, form=UNCHANGED,
                 content_type=UNCHANGED, headers=UNCHANGED, as_=UNCHANGED,
                 query=UNCHANGED, description=None, extra_environ=UNCHANGED,
                 response: Response=None, authorization=UNCHANGED):

        self.base_call = base_call
        self.diff = {}
        super().__init__(title, description=description, response=response)

        self.url = url
        if url_parameters is not UNCHANGED:
            self.url_parameters = url_parameters

        if query is not UNCHANGED:
            self.query = query

        self.extra_environ = extra_environ
        self.verb = verb
        self.form = form
        self.content_type = content_type
        self.authorization = authorization
        self.headers = headers
        self.as_ = as_

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
    def url(self):
        return self.diff.get('url', self.base_call.url)

    @url.setter
    def url(self, value):
        if value is UNCHANGED:
            self.diff.pop('url', None)
            return

        url, url_parameters, query = self.extract_url_parameters(value)
        if url and url != self.base_call.url:
            self.diff['url'] = url
            self.url_parameters = url_parameters
            self.query = query

    @property
    def url_parameters(self):
        return self.diff.get('url_parameters', self.base_call.url_parameters)

    @url_parameters.setter
    def url_parameters(self, value):
        self.update_diff('url_parameters', value)

    @url_parameters.deleter
    def url_parameters(self):
        del self.diff['url_parameters']

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
        self.update_diff('headers', value if value is UNCHANGED else HeaderSet(value))

    @headers.deleter
    def headers(self):
        del self.diff['headers']

    @property
    def query(self):
        return self.diff.get('query', self.base_call.query)

    @query.setter
    def query(self, value):
        self.update_diff('query', value if value is UNCHANGED else normalize_query_string(value))

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
    def form(self):
        return self.diff.get('form', self.base_call.form)

    @form.setter
    def form(self, value):
        self.update_diff('form', value)

    @form.deleter
    def form(self):
        del self.diff['form']

