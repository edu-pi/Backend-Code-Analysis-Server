import ast

from app.analysis.element_manager import CodeElementManager
from app.analysis.generator.parser.call_parser import CallParser, Print
from app.analysis.highlight import expressions_highlight_indices
from app.analysis.models import PrintViz


class ExprGenerator:
    # ast.Expr : 함수 호출과 같은 식이 반환 값으로 사용되지 않거나, 저장되지 않는 상태에서 그 자체문으로 나타나는 경우의 타입
    def __init__(self, node: ast.Expr, elem_manager: CodeElementManager):
        self.__call_id = elem_manager.get_call_id(node)
        self.__value = node.value
        self.__elem_manager = elem_manager

    @staticmethod
    def generate(node: ast.Expr, elem_manager: CodeElementManager):
        expr_generator = ExprGenerator(node, elem_manager)
        return expr_generator.__get_parse_value()

    def __get_parse_value(self):
        if isinstance(self.__value, ast.Name):
            return
        elif isinstance(self.__value, ast.Constant):
            return
        elif isinstance(self.__value, ast.BinOp):
            return
        elif isinstance(self.__value, ast.Call):
            call_obj = CallParser.parse(self.__value, self.__elem_manager)
            return self.__convert_call_obj_to_vizs(call_obj)
        elif isinstance(self.__value, ast.Lambda):
            return
        else:
            raise TypeError(f"[ExprGe]:{type(self.__value)}는 정의되지 않았습니다.")

    def __convert_call_obj_to_vizs(self, call_obj):
        """
        Call 객체를 List[Viz] 객체로 변환
        """
        if isinstance(call_obj, Print):
            return self.__convert_print_obj_to_print_vizs(call_obj)
        else:
            raise TypeError(f"[ExprGe]:{type(call_obj)}는 정의되지 않았습니다.")

    def __convert_print_obj_to_print_vizs(self, print_obj: Print):
        """
        Print 객체를 List[PrintViz] 객체로 반환
        """
        # 하이라이트 속성 추출
        highlights = expressions_highlight_indices(print_obj.expressions)

        print_vizs = [
            PrintViz(
                id=self.__call_id,
                depth=self.__elem_manager.get_depth(),
                expr=print_obj.expressions[idx],
                highlight=highlights[idx],
                console=print_obj.console if idx == len(print_obj.expressions) - 1 else None
            )
            for idx in range(len(print_obj.expressions))
        ]
        return print_vizs
