import ast

from fastapi import FastAPI

from app.analysis.code_analyzer import CodeAnalyzer
from app.analysis.element_manager import CodeElementManager

app = FastAPI()


@app.post("/v1/python")
def read_root(source_code):
    # 코드 분석 인스턴스 생성
    code_analyzer = CodeAnalyzer(CodeElementManager())

    # 소스 코드를 추상 구문 트리로 변환
    parsed_ast = ast.parse(source_code)

    return code_analyzer.visualize_code(parsed_ast)
