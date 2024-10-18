from fastapi import FastAPI
from starlette.responses import JSONResponse

from app.models.request_code import RequestCode
from app.visualize.code_visualizer import CodeVisualizer

app = FastAPI()


@app.get("/edupi-visualize/health-check")
def root():
    return JSONResponse(status_code=200, content="ok")


@app.post("/edupi-visualize/v1/python")
def read_root(request_code: RequestCode):
    # 코드 분석 인스턴스 생성
    code_analyzer = CodeVisualizer(request_code)

    return code_analyzer.visualize_code()
