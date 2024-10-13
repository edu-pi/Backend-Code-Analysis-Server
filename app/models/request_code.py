from pydantic import BaseModel


class RequestCode(BaseModel):
    source_code: str
    input: list

    def __init__(self, source_code: str, input: str):
        # 부모 클래스의 __init__ 호출 (BaseModel 초기화)
        super().__init__(source_code=source_code, input=input.split("\n"))
