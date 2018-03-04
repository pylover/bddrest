
class CallVerifyError(Exception):
    pass


class ValidationError(ValueError):
    pass


class InvalidUrlParametersError(ValidationError):
    pass

