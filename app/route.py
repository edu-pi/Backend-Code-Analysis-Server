import ast

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from app.visualize.analysis.element_manager import CodeElementManager
from app.visualize.code_visualizer import CodeVisualizer

app = FastAPI()

origins = [
    "*",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class RequestCode(BaseModel):
    source_code: str


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.post("/v1/python")
def read_root(request_code: RequestCode):
    # 코드 분석 인스턴스 생성
    code_analyzer = CodeVisualizer(request_code)

    return code_analyzer.visualize_code()
