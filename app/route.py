from fastapi import FastAPI
from pydantic import BaseModel

from app.visualize.code_visualizer import CodeVisualizer

app = FastAPI()


class RequestCode(BaseModel):
    source_code: str


@app.get("/edupi_visualize/")
def read_root():
    return {"Hello": "World"}


@app.post("/edupi_visualize/v1/python")
def read_root(request_code: RequestCode):
    # 코드 분석 인스턴스 생성
    code_analyzer = CodeVisualizer(request_code.source_code)

    return code_analyzer.visualize_code()
