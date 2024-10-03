from enum import Enum


class ErrorEnum(Enum):

    # 400
    CODE_EXEC_ERROR = "CS-400001", "지원하지 않는 형식입니다."
    INPUT_SIZE_MATCHING_ERROR = "CS-400002", "입력한 개수가 일치하지 않습니다."
    CODE_SYNTAX_ERROR = "CS-400003", "잘못된 문법입니다."

    def __init__(self, code, detail):
        self.code = code
        self.detail = detail

    def to_dict(self):
        return {
            "code": self.code,
            "detail": self.detail,
        }
