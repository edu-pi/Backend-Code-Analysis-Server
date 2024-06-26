import ast
import re
from dataclasses import dataclass
from typing import Any

from app.visualize.analysis.element_manager import CodeElementManager
from app.visualize.analysis.stmt_parser.expr_analysis.expr_models.expr_obj import ExprObj
from app.visualize.analysis.stmt_parser.expr_analysis.expr_util import util
from app.visualize.analysis.stmt_parser.expr_analysis.expr_util.util import replace_word, transpose_with_last_fill


class BinopAnalyzer:

    @staticmethod
    def parse(left_obj: ExprObj, right_obj: ExprObj, op: ast, elem_manager: CodeElementManager):
        value = BinopAnalyzer._calculate_value(left_obj.value, right_obj.value, op)
        # expressions = BinopAnalyzer._create_expressions(value, ast.unparse(left), elem_manager)

        return ExprObj(type="binop", value=value, expressions=expressions)

    # 왼쪽 오른쪽 값으로 연산식 계산
    @staticmethod
    def _calculate_value(left_value, right_value, op: ast):
        if isinstance(op, ast.Add):
            return left_value + right_value

        elif isinstance(op, ast.Sub):
            return left_value - right_value

        elif isinstance(op, ast.Mult):
            return left_value * right_value

        elif isinstance(op, ast.Div):  # '/'
            return left_value / right_value  # 실수로 계산

        elif isinstance(op, ast.FloorDiv):  # '//'
            return left_value // right_value  # 정수로 계산

        else:
            raise TypeError(f"[call_travel] {type(op)}는 잘못된 타입입니다.")

    # 1 + 2
    # a + 2
    # a + b
    # a + b + c
    # a + sum([1, 2])
    @staticmethod
    def _create_expressions(left_obj, right_obj, op):
        total_expressions = util.transpose_with_last_fill([left_obj, right_obj])

        for i in range(len(total_expressions)):
            total_expressions[i] = f"{total_expressions[i][0]} {op} {total_expressions[i][1]}"

    # 연산식을 따라가면서 계산해 결과를 반환
    @staticmethod
    def _create_expressions(result_value: int, initial_expression: str, elem_manager: CodeElementManager):
        # 초기 계산식 저장
        expressions = [initial_expression]
        pattern = r"\b[a-zA-Z_]\w*\b"

        # 변수 이름 추출
        target_names = set(re.findall(pattern, initial_expression))
        next_expression = initial_expression

        # 변수들을 값으로 대체
        for original_name in target_names:
            replace_value = elem_manager.get_variable_value(original_name)
            next_expression = replace_word(
                expression=next_expression, original_word=original_name, new_word=replace_value
            )

        if len(target_names) != 0:
            expressions.append(next_expression)

        # 마지막 계산 결과 저장
        expressions.append(str(result_value))

        return expressions


@dataclass
class Binop:
    value: Any
    expressions: list[str]
