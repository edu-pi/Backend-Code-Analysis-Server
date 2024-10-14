from fastapi import FastAPI
from pydantic import BaseModel

from app.visualize.code_visualizer import CodeVisualizer
from app.web import exception_handler
from app.web.logger import log_request, log_response

app = FastAPI()

# 미들웨어 등록
app.middleware("http")(log_request)
app.middleware("http")(log_response)

# 핸들러 등록
exception_handler.setup_exception_handlers(app)


class RequestCode(BaseModel):
    source_code: str


@app.get("/edupi-visualize")
def read_root():
    return {"Hello": "World"}


@app.post("/edupi-visualize/v1/python")
def read_root(request_code: RequestCode):
    # 코드 분석 인스턴스 생성
    code_analyzer = CodeVisualizer(request_code.source_code)

    return code_analyzer.visualize_code()
