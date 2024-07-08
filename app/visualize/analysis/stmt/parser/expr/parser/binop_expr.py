import ast

from app.visualize.analysis.stmt.parser.expr.models.expr_obj import ExprObj, BinopObj
from app.visualize.utils.util import Util


class BinopExpr:

    @staticmethod
    def parse(left_obj: ExprObj, right_obj: ExprObj, op: ast):
        value = BinopExpr._calculate_value(left_obj.value, right_obj.value, op)
        expressions = BinopExpr._create_expressions(left_obj.expressions, right_obj.expressions, op, value)

        return BinopObj(value=value, expressions=expressions)

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
    def _create_expressions(left_expressions, right_expressions, op, value) -> tuple:
        total_expressions = Util.transpose_with_last_fill([left_expressions, right_expressions])

        for i in range(len(total_expressions)):
            total_expressions[i] = BinopExpr._concat_expression(total_expressions[i][0], total_expressions[i][1], op)

        if isinstance(value, str):
            total_expressions.append(f"'{value}'")
        else:
            total_expressions.append(str(value))

        return tuple(total_expressions)

    @staticmethod
    def _concat_expression(left_expression, right_expression, op: ast):
        if isinstance(op, ast.Add):
            return f"{left_expression} + {right_expression}"

        elif isinstance(op, ast.Sub):
            return f"{left_expression} - {right_expression}"

        elif isinstance(op, ast.Mult):
            return f"{left_expression} * {right_expression}"

        elif isinstance(op, ast.Div):
            return f"{left_expression} / {right_expression}"

        elif isinstance(op, ast.FloorDiv):
            return f"{left_expression} // {right_expression}"

        else:
            raise TypeError(f"[call_travel] {type(op)}는 잘못된 타입입니다.")
