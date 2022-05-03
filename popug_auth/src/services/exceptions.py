class BaseServiceException(Exception):
    pass


class UserNotFound(BaseServiceException):
    pass


class AuthorizationCodeInvalid(BaseServiceException):
    pass


class InvalidTokenException(BaseServiceException):
    pass
