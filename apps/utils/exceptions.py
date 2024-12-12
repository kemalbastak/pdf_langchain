from fastapi import HTTPException
from starlette.status import (HTTP_400_BAD_REQUEST, HTTP_401_UNAUTHORIZED, HTTP_403_FORBIDDEN, HTTP_404_NOT_FOUND,
                              HTTP_409_CONFLICT, HTTP_500_INTERNAL_SERVER_ERROR, HTTP_503_SERVICE_UNAVAILABLE)


class BadRequestError(HTTPException):
    def __init__(self, detail: str = "Bad request"):
        super().__init__(status_code=HTTP_400_BAD_REQUEST, detail=detail)


class UnauthorizedError(HTTPException):
    def __init__(self, detail: str = "Unauthorized access"):
        super().__init__(status_code=HTTP_401_UNAUTHORIZED, detail=detail)


class ForbiddenError(HTTPException):
    def __init__(self, detail: str = "Forbidden access"):
        super().__init__(status_code=HTTP_403_FORBIDDEN, detail=detail)


class NotFoundError(HTTPException):
    def __init__(self, detail: str = "Resource not found"):
        super().__init__(status_code=HTTP_404_NOT_FOUND, detail=detail)


class InternalServerError(HTTPException):
    def __init__(self, detail: str = "Internal server error"):
        super().__init__(status_code=HTTP_500_INTERNAL_SERVER_ERROR, detail=detail)


class ValidationError(HTTPException):
    def __init__(self, detail: str = "Validation failed"):
        super().__init__(status_code=HTTP_400_BAD_REQUEST, detail=detail)


class ConflictError(HTTPException):
    def __init__(self, detail: str = "Conflict detected"):
        super().__init__(status_code=HTTP_409_CONFLICT, detail=detail)  # 409 Conflict


class ServiceUnavailableError(HTTPException):
    def __init__(self, detail: str = "Service is temporarily unavailable"):
        super().__init__(status_code=HTTP_503_SERVICE_UNAVAILABLE, detail=detail)  # 503 Service Unavailable
