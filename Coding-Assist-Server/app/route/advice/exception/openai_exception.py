from starlette import status

from app.web.exception.base_exception import BaseCustomException
from app.web.exception.enum.error_enum import ErrorEnum


class OpenaiException(BaseCustomException):
    def __init__(self, error_enum: ErrorEnum, result: dict = None):
        super().__init__(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            error_enum=error_enum,
            result={} if result is None else result
        )