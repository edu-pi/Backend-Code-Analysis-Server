# 시각화에 필요한 Expr를 만듦
import ast

from app.analysis.element_manager import CodeElementManager
from app.analysis.generator.parser.call_parser import CallParser, Print
from app.analysis.highlight import expressions_highlight_indices
from app.analysis.models import PrintViz


class ExprGenerator:
    # ast.Expr : 함수 호출과 같은 식이 반환 값으로 사용되지 않거나, 저장되지 않는 상태에서 그 자체문으로 나타나는 경우의 타입
    def __init__(self, node: ast.Expr, elem_manager: CodeElementManager):
        self.value = node.value
        self.elem_manager = elem_manager

    @staticmethod
    def generate(node: ast.Expr, elem_manager: CodeElementManager):
        expr_generator = ExprGenerator(node, elem_manager)

        if isinstance(node.value, ast.Name):
            return node
        elif isinstance(node.value, ast.Constant):
            return node
        elif isinstance(node.value, ast.BinOp):
            return
        # ast.Call 처리
        elif isinstance(node.value, ast.Call):
            call_obj = CallParser(node.value, elem_manager).parse()
            return expr_generator.convert_call_obj_to_vizs(call_obj)
        elif isinstance(node.value, ast.Lambda):
            return node
        else:
            raise TypeError(f"[ExprGe]:{type(node.value)}는 정의되지 않았습니다.")

    def convert_call_obj_to_vizs(self, call_obj):
        """
        Call 객체를 List[Viz] 객체로 변환
        """
        if isinstance(call_obj, Print):
            return self.convert_print_obj_to_print_vizs(call_obj)
        else:
            raise TypeError(f"[ExprGe]:{type(call_obj)}는 정의되지 않았습니다.")

    def convert_print_obj_to_print_vizs(self, print_obj: Print):
        """
        Print 객체를 List[PrintViz] 객체로 반환
        """
        # 하이라이트 속성 추출
        highlights = expressions_highlight_indices(print_obj.expressions)

        print_vizs = [
            PrintViz(
                id=self.elem_manager.get_call_id(self),
                depth=self.elem_manager.get_depth(),
                expr=expression,
                highlight=highlight
            )
            for expression, highlight in zip(print_obj.expressions, highlights)
        ]
        return print_vizs

