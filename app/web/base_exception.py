from starlette import status

from app.execute.exception.error_enum import ErrorEnum


class BaseCustomException(Exception):
    def __init__(self, status_code: status, error_enum: ErrorEnum, result: dict = None):
        self.status_code = status_code
        self.error_enum = error_enum
        self.result = {} if result is None else result
