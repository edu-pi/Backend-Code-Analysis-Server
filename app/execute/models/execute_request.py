from pydantic import BaseModel


class ExecuteRequest(BaseModel):
    source_code: str
    input: str
