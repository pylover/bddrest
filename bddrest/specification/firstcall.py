from ..headerset import HeaderSet
from ..helpers import normalize_query_string
from .call import Call


class FirstCall(Call):

    _headers = None
    _url = None
    _url_parameters = None
    _verb = None
    _query = None
    _form = None
    _json = None
    _multipart = None
    _as = None
    _extra_environ = None

    # FIXME: remove them  and use header set to store it.
    _content_type = None
    _authorization = None

    _body = None

    def __init__(self, url='/', verb='GET', url_parameters=None, form=None,
                 json=None, multipart=None, content_type=None, headers=None,
                 as_=None, query=None, title=None, description=None,
                 extra_environ=None, response=None,
                 authorization=None, body=None):

        super().__init__(
            title=title,
            description=description,
            response=response
        )

        self.url = url
        # the `url_parameters` and `query` attributes may be set by the url
        # setter. so we're not going to override them anyway.
        if url_parameters is not None:
            self.url_parameters = url_parameters

        if query is not None:
            self.query = query

        self.verb = verb
        if body is not None:
            self.body = body
        else:
            self.form = form
            self.multipart = multipart
            self.json = json

        self.content_type = content_type
        self.authorization = authorization
        self.headers = headers
        self.as_ = as_
        self.extra_environ = extra_environ

    @property
    def url(self):
        return self._url

    @url.setter
    def url(self, value):
        self._url, self.url_parameters, self.query = \
            self.extract_url_parameters(value)

    @property
    def url_parameters(self):
        return self._url_parameters

    @url_parameters.setter
    def url_parameters(self, value):
        self._url_parameters = value

    @property
    def verb(self):
        return self._verb

    @verb.setter
    def verb(self, value):
        self._verb = value

    @property
    def headers(self):
        return self._headers

    @headers.setter
    def headers(self, value):
        self._headers = HeaderSet(value) if value is not None else None

    @property
    def query(self):
        return self._query

    @query.setter
    def query(self, value):
        self._query = normalize_query_string(value)

    @property
    def content_type(self):
        return self._content_type

    @content_type.setter
    def content_type(self, value):
        self._content_type = value

    @property
    def authorization(self):
        return self._authorization

    @authorization.setter
    def authorization(self, value):
        self._authorization = value

    @property
    def as_(self):
        return self._as

    @as_.setter
    def as_(self, value):
        self._as = value

    @property
    def extra_environ(self):
        return self._extra_environ

    @extra_environ.setter
    def extra_environ(self, value):
        self._extra_environ = value

    @property
    def body(self):
        return self._body

    @body.setter
    def body(self, value):
        self._body = value

    @property
    def form(self):
        return self._form

    @form.setter
    def form(self, value):
        self._form = value

    @property
    def json(self):
        return self._json

    @json.setter
    def json(self, value):
        self._json = value

    @property
    def multipart(self):
        return self._multipart

    @multipart.setter
    def multipart(self, value):
        self._multipart = value
