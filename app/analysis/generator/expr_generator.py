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

    def generate(self):
        if isinstance(self.value, ast.Name):
            return self
        elif isinstance(self.value, ast.Constant):
            return self
        elif isinstance(self.value, ast.BinOp):
            return self
        # 함수
        elif isinstance(self.value, ast.Call):
            call_parser = CallParser(self.value, self.elem_manager)
            return self.transfer_call_objs_to_viz_objs(call_parser.parse())
        elif isinstance(self.value, ast.Lambda):
            return self
        else:
            raise TypeError(f"[ExprGe]:{type(self.value)}는 정의되지 않았습니다.")

    def transfer_call_objs_to_viz_objs(self, calls: list):
        """
        Call 객체를 시각화하는 Viz 객체로 변환
        Args:
            calls: call_parser를 통해 생성된 list[Call] 객체

        Returns:
            list[PrintViz]: 시각화된 Viz 객체
        """
        if isinstance(calls[0], Print):
            return self.transfer_print_objs_to_viz_objs(calls)
        else:
            raise TypeError(f"[ExprGe]:{type(calls)}는 정의되지 않았습니다.")

    def transfer_print_objs_to_viz_objs(self, print_objs: list[Print]):
        """
        Print 객체를 시각화하는 PrintViz 객체로 변환
        Args:
            print_objs:  call_parser를 통해 생성된 list[Print] 객체

        Returns:
            list[PrintViz]: 시각화된 PrintViz 객체
        """
        parsed_expressions = []
        # print_objs에 있는 모든 expressions를 expressions에 추가
        for print_obj in print_objs:
            parsed_expressions.append(print_obj.expressions)

        # 하이라이트 속성 추출
        highlights = expressions_highlight_indices(parsed_expressions)

        print_vizs = [
            PrintViz(
                id=self.elem_manager.get_call_id(self),
                depth=self.elem_manager.get_depth(),
                expr=expression,
                highlight=highlight
            )
            for expression, highlight in zip(parsed_expressions, highlights)
        ]
        return print_vizs

