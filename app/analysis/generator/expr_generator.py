# 시각화에 필요한 Expr를 만듦
import ast

from app.analysis.element_manager import CodeElementManager
from app.analysis.generator.parser.call_parser import CallParser


class ExprGenerator:
    # ast.Expr : 함수 호출과 같은 식이 반환 값으로 사용되지 않거나, 저장되지 않는 상태에서 그 자체문으로 나타나는 경우의 타입
    def __init__(self, node: ast.Expr, elem_manager: CodeElementManager):
        self.value = node.value
        self.elem_manager = elem_manager

    def generate(self):
        if isinstance(self.value, ast.Name):
            return self
        elif isinstance(self.value, ast.Constant):
            return self
        elif isinstance(self.value, ast.BinOp):
            return self
        elif isinstance(self.value, ast.Call):
            CallParser(self.value, self.elem_manager).parse()
            return self
        elif isinstance(self.value, ast.Lambda):
            return self
        else:
            raise TypeError(f"{type(self.value)}는 정의되지 않았습니다.")

