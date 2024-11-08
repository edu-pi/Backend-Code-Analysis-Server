import logging

from fastapi import FastAPI, Request
from starlette import status
from starlette.responses import JSONResponse

from app.web.exception.code_visualize_error import CodeVisualizeError
from app.web.exception.error_enum import ErrorEnum
from app.web.models.error_response import ErrorResponse


def setup_exception_handlers(app: FastAPI):
    @app.exception_handler(CodeVisualizeError)
    async def code_execute_exception_handler(request: Request, exc: CodeVisualizeError):
        response = ErrorResponse(code=exc.error_enum.code, detail=exc.error_enum.detail, result=exc.result)
        return JSONResponse(status_code=exc.status_code, content=response.to_dict())

    @app.exception_handler(NotImplementedError)
    async def code_execute_exception_handler(request: Request, exc: NotImplementedError):
        logging.error(f"[NotImplementedError Exception] : {exc.args}")
        response = ErrorResponse(code=ErrorEnum.NOT_SUPPORTED_VISUALIZE.code,
                                 detail=ErrorEnum.NOT_SUPPORTED_VISUALIZE.detail)

        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content=response.to_dict())
    
    @app.exception_handler(Exception)
    async def code_exception_handler(request: Request, exc: Exception):
        logging.error(f"[Unknown Exception] : {exc.args}")
        response = ErrorResponse(code=ErrorEnum.NOT_SUPPORTED_VISUALIZE.code,
                                 detail=ErrorEnum.NOT_SUPPORTED_VISUALIZE.detail)

        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content=response.to_dict())
