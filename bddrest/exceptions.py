class CallVerifyError(Exception):
    pass


class ValidationError(ValueError):
    pass


class InvalidUrlParametersError(ValidationError):
    pass


rawurl_exc = ValueError(
    "`path`, `path_parameters` and `query` are cannot set when `rawurl` is "
    "passed"
)
