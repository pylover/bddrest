from .call import Call
from .headerset import HeaderSet


class When(Call):
    def __init__(self, base_call, title: str, description=None, response=None,
                 headers=None, **diff):
        self.base_call = base_call
        super().__init__(title, description=description, response=response)

        if 'url' in diff:
            diff['url'], url_parameters, query = self.extract_url_parameters(diff['url'])
            if 'url_parameters' not in diff:
                diff['url_parameters'] = url_parameters

            if 'query' not in diff:
                diff['query'] = normalize_query_string(query)

        self.diff = diff
        self.headers = headers

    def to_dict(self):
        result = dict(title=self.title)
        result.update(self.diff)

        if self.description is not None:
            result['description'] = self.description

        if self.response is not None:
            result['response'] = self.response.to_dict()

        return result

    def update_diff(self, key, value):
        if not value:
            self.diff.pop(key, None)
        else:
            self.diff[key] = value

    @property
    def url(self):
        return self.diff.get('url', self.base_call.url)

    @url.setter
    def url(self, value):
        url, self.url_parameters, self.query = self.extract_url_parameters(value)
        if url:
            self.diff['url']
        else:
            self.diff.pop('url', None)

    @property
    def url_parameters(self):
        return self.diff.get('url_parameters', self.base_call.url_parameters)

    @url_parameters.setter
    def url_parameters(self, value):
        self.update_diff('url_parameters', value)

    @property
    def verb(self):
        return self.diff.get('verb', self.base_call.verb)

    @verb.setter
    def verb(self, value):
        self.update_diff('verb', value)

    @property
    def headers(self):
        return self.diff.get('headers', self.base_call.headers)

    @headers.setter
    def headers(self, value):
        self.update_diff('headers', HeaderSet(value) if value is not None else None)

    @property
    def query(self):
        return self.diff.get('query', self.base_call.query)

    @query.setter
    def query(self, value):
        self.update_diff('query', normalize_query_string(value))

    @property
    def content_type(self):
        return self.diff.get('content_type', self.base_call.content_type)

    @content_type.setter
    def content_type(self, value):
        self.update_diff('content_type', value)

    @property
    def as_(self):
        return self.diff.get('as_', self.base_call.as_)

    @as_.setter
    def as_(self, value):
        self.update_diff('as_', value)

    @property
    def extra_environ(self):
        return self.diff.get('extra_environ', self.base_call.extra_environ)

    @extra_environ.setter
    def extra_environ(self, value):
        self.update_diff('extra_environ', value)

    @property
    def form(self):
        return self.diff.get('form', self.base_call.form)

    @form.setter
    def form(self, value):
        self.update_diff('form', value)

