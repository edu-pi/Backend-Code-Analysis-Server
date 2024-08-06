from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from py_eureka_client import eureka_client
from pydantic import BaseModel

from app.visualize.code_visualizer import CodeVisualizer


async def init_eureka():
    await eureka_client.init_async(
        eureka_server="http://localhost:8761/eureka/", app_name="edupi-visualize", instance_port=8081, on_error=on_error
    )


def on_error(err_type: str, err: Exception):
    print(err_type, err, sep=": ")


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_eureka()
    yield


app = FastAPI(lifespan=lifespan)


origins = [
    "*",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class RequestCode(BaseModel):
    source_code: str


@app.get("/edupi_visualize/v1/")
def read_root():
    return {"Hello": "World"}


@app.post("/edupi_visualize/v1/python")
def read_root(request_code: RequestCode):
    # 코드 분석 인스턴스 생성
    code_analyzer = CodeVisualizer(request_code.source_code)

    return code_analyzer.visualize_code()
