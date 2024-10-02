class SuccessResponse:
    def __init__(self, detail: str, result: dict = None):
        self.code = "CS-200000"
        self.detail = detail
        self.result = result

    def to_dict(self):
        # Convert the response object to a dictionary
        return {
            "code": self.code,
            "detail": self.detail,
            "result": self.result,
        }
