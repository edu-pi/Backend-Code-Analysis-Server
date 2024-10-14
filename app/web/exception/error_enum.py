from enum import Enum


class ErrorEnum(Enum):

    # 400
    CODE_EXEC_ERROR = "CS-400001", "지원하지 않는 형식입니다."

    def __init__(self, code, detail):
        self.code = code
        self.detail = detail

    def to_dict(self):
        return {
            "code": self.code,
            "detail": self.detail,
        }
