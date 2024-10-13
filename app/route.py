from fastapi import FastAPI

from app.models.request_code import RequestCode
from app.visualize.code_visualizer import CodeVisualizer

app = FastAPI()


@app.get("/edupi-visualize")
def read_root():
    return {"Hello": "World"}


@app.post("/edupi-visualize/v1/python")
def read_root(request_code: RequestCode):
    # 코드 분석 인스턴스 생성
    code_analyzer = CodeVisualizer(request_code)

    return code_analyzer.visualize_code()
