from fastapi import FastAPI
from pydantic import BaseModel
from starlette.responses import JSONResponse

from app.execute.executor import Executor
from app.execute.models.execute_request import ExecuteRequest
from app.visualize.code_visualizer import CodeVisualizer
from app.web import exception_handler
from app.web.models.success_reponse import SuccessResponse

app = FastAPI()


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


@app.post("/edupi-visualize/v1/execute")
def run(run_request: ExecuteRequest):
    # 코드 분석 인스턴스 생성
    executor = Executor(run_request.source_code, run_request.input)
    result = executor.execute_user_code()

    success_response = SuccessResponse(detail="success run", result={"output": result})

    return JSONResponse(status_code=200, content=success_response.to_dict())
