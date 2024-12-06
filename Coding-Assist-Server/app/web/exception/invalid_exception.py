from starlette.status import HTTP_400_BAD_REQUEST

from app.web.exception.base_exception import BaseCustomException
from app.web.exception.enum.error_enum import ErrorEnum


class InvalidException(BaseCustomException):
    def __init__(self, error_enum: ErrorEnum, result: dict = None):
        super().__init__(
            status_code=HTTP_400_BAD_REQUEST,
            error_enum=error_enum,
            result={} if result is None else result
        )

