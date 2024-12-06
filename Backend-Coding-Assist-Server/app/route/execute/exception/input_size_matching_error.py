from starlette import status

from app.web.exception.base_exception import BaseCustomException
from app.web.exception.enum.error_enum import ErrorEnum


class InputSizeMatchingError(BaseCustomException):
    def __init__(self, error_enum: ErrorEnum, result: dict = None):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            error_enum=error_enum,
            result={} if result is None else result,
        )
