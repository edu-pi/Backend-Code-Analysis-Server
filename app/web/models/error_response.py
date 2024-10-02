class ErrorResponse:
    def __init__(self, code: str, detail: str, result=None):
        self.code = code
        self.detail = detail
        self.result = {} if result is None else result

    def to_dict(self):
        # Convert the response object to a dictionary
        return {
            "code": self.code,
            "detail": self.detail,
            "result": self.result,
        }
