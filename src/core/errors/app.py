from .base import BaseAppException


class NotFound(BaseAppException):
    code = "NOT_FOUND"
    status_code = 404


class Conflict(BaseAppException):
    code = "CONFLICT"
    status_code = 409


class Unauthorized(BaseAppException):
    code = "UNAUTHORIZED"
    status_code = 401


class Forbidden(BaseAppException):
    code = "FORBIDDEN"
    status_code = 403


class ServiceUnavailable(BaseAppException):
    code = "SERVICE_UNAVAILABLE"
    status_code = 503


class InternalError(BaseAppException):
    code = "INTERNAL_SERVER_ERROR"
    status_code = 500
