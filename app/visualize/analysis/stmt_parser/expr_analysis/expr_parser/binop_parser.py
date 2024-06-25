import ast
import re

from app.visualize.analysis.element_manager import CodeElementManager
from app.visualize.analysis.stmt_parser.expr_analysis.expr_util.util import replace_word


class BinopAnalyzer:

    @staticmethod
    def parse(left, right, op: ast, elem_manager: CodeElementManager):
        value = BinopAnalyzer._calculate_value(left, right, op)
        expressions = BinopAnalyzer._create_expressions(value, ast.unparse(left), elem_manager)

        return {"value": value, "expressions": expressions}

    # 왼쪽 오른쪽 값으로 연산식 계산
    @staticmethod
    def _calculate_value(left, right, op: ast):
        if isinstance(op, ast.Add):
            return left + right

        elif isinstance(op, ast.Sub):
            return left - right

        elif isinstance(op, ast.Mult):
            return left * right

        elif isinstance(op, ast.Div):  # '/'
            return left / right  # 실수로 계산

        elif isinstance(op, ast.FloorDiv):  # '//'
            return left // right  # 정수로 계산

        else:
            raise TypeError(f"[call_travel] {type(op)}는 잘못된 타입입니다.")

    # 연산식을 따라가면서 계산해 결과를 반환
    @staticmethod
    def _create_expressions(result_value: int, initial_expression: str, elem_manager: CodeElementManager):
        # 초기 계산식 저장
        expressions = [initial_expression]
        pattern = r'\b[a-zA-Z_]\w*\b'

        # 변수 이름 추출
        target_names = set(re.findall(pattern, initial_expression))
        next_expression = initial_expression

        # 변수들을 값으로 대체
        for original_name in target_names:
            replace_value = elem_manager.get_variable_value(original_name)
            next_expression = replace_word(expression=next_expression, original_word=original_name,
                                           new_word=replace_value)

        if len(target_names) != 0:
            expressions.append(next_expression)

        # 마지막 계산 결과 저장
        expressions.append(str(result_value))

        return expressions
