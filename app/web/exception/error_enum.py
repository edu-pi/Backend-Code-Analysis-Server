from enum import Enum


class ErrorEnum(Enum):

    # 400
    NOT_SUPPORTED_VISUALIZE = "CV-400001", "It contains syntax that we can't visualize yet."
    VISUALIZE_TIMEOUT = "CV-400002", "The code is too long."

    def __init__(self, code, detail):
        self.code = code
        self.detail = detail

    def to_dict(self):
        return {
            "code": self.code,
            "detail": self.detail,
        }
