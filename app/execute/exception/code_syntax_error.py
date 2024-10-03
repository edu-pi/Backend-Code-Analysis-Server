from starlette import status

from app.execute.exception.error_enum import ErrorEnum
from app.web.base_exception import BaseCustomException


class CodeSyntaxError(BaseCustomException):
    def __init__(self, error_enum: ErrorEnum, result: dict = None):
        super().__init__(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            error_enum=error_enum,
            result={} if result is None else result,
        )
