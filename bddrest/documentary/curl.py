
class CURL:
    def __init__(
        self,
        url,
        form,
        query,
        authorization,
        verb='GET',
        content_type='text/plain',
        headers=[]
    ):
        self.parts = ['curl']
        self.add_url(url)
        self.add_verb(verb)
        self.add_headers(headers)
        self.add_content_type(content_type)
        if form is not None:
            self.add_form(form)
        if query is not None:
            self.add_query(query)
        if authorization is not None:
            self.add_authorization(authorization)

    def __repr__(self):
        return ' '.join(self.parts)

    def add_url(self, url):
        self.parts.append(url)

    def add_verb(self, verb):
        self.parts.append(f'-X {verb}')

    def add_form(self, form):
        for k, v in form.items():
            self.parts.append(f'-F "{k}={v}"')

    def add_headers(self, headers):
        for header in headers:
            self.parts.append(f'-H "{header}"')

    def add_content_type(self, content_type):
        self.parts.append(f'-H "Content-Type: {content_type}"')

    def add_authorization(self, authorization):
        self.parts.append(f'-H "Authorization: {authorization}"')

    #TODO: Add this
    def add_query(self, query):
        pass


#    @classmethod
#    def from_call(cls, call: Call) -> 'CURL':
#        raise NotImplementedError
