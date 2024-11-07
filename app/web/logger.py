from datetime import datetime
from fastapi import Request
from starlette.concurrency import iterate_in_threadpool
import logging

logger = logging.getLogger("uvicorn.logger")

if not logger.hasHandlers():
    logger.setLevel(logging.INFO)

    # 콘솔 핸들러 및 포맷 설정
    handler = logging.StreamHandler()
    handler.setLevel(logging.INFO)
    logger.addHandler(handler)


def get_logger():
    return logger


# Request 로깅 미들웨어
async def log_request(request: Request, call_next):
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    body = await request.body()
    logger.info(f"[{current_time}] Request: {request.method} {request.url}  {body.decode()}")

    response = await call_next(request)
    return response


# Response 로깅 미들웨어
async def log_response(request: Request, call_next):
    response = await call_next(request)

    # 응답 바디 로깅
    response_body = [chunk async for chunk in response.body_iterator]
    response.body_iterator = iterate_in_threadpool(iter(response_body))

    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    logger.info(f"[{current_time}] Response : {response.status_code} {response_body[0].decode()}")

    return response
