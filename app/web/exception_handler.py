from fastapi import FastAPI, Request
from starlette.responses import JSONResponse

from app.web.exception.code_execute_error import CodeExecuteError
from app.web.models.error_response import ErrorResponse


def setup_exception_handlers(app: FastAPI):
    @app.exception_handler(CodeExecuteError)
    async def code_execute_exception_handler(request: Request, exc: CodeExecuteError):
        response = ErrorResponse(code=exc.error_enum.code, detail=exc.error_enum.detail, result=exc.result)
        return JSONResponse(status_code=exc.status_code, content=response.to_dict())
