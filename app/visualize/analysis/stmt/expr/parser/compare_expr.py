import ast

from app.visualize.analysis.stmt.expr.expr_util import util
from app.visualize.analysis.stmt.expr.expr_util.util import list_to_str
from app.visualize.analysis.stmt.expr.model.expr_obj import ExprObj, CompareObj


class CompareExpr:

    @staticmethod
    def parse(left_obj: ExprObj, comparators: tuple[ExprObj, ...], ops: tuple[ast.cmpop, ...]):
        value = CompareExpr._get_final_calculate_value(left_obj, comparators, ops)
        expressions = CompareExpr._get_expressions(left_obj, comparators, ops)

        return CompareObj(value=value, expressions=expressions)

    @staticmethod
    def _get_final_calculate_value(left_obj: ExprObj, comparators: tuple[ExprObj, ...], ops: tuple[ast.cmpop, ...]):
        left_value = left_obj.value
        # 피연자 값과 비교 연산자를 순차적으로 계산
        for idx, comparator_obj in enumerate(comparators):
            right_value = comparator_obj.value
            if not CompareExpr._calculate_value(left_value, right_value, ops[idx]):
                return False
            left_value = right_value
        return True

    @staticmethod
    def _get_expressions(left_obj: ExprObj, comparators: tuple[ExprObj, ...], ops: tuple[ast.cmpop, ...]):
        total_expressions = []
        # 피연자 값과 비교 연산자를 순차적으로 계산
        if len(comparators) <= 1:  # 비교 연산자가 1개 이하인 경우, 자세한 표현 과정 반환
            total_expressions.extend(CompareExpr._create_expressions(left_obj, comparators[0], ops[0]))

        else:  # 비교 연산자가 2개 이상인 경우, 생략된 표현 과정 반환
            total_expressions.append(CompareExpr._create_origin_expression(left_obj, comparators, ops))

        # 최종 결과값 추가
        total_expressions.append(str(value))
        return tuple(total_expressions)

    @staticmethod
    def _calculate_value(left_value, right_value, op: ast.cmpop):
        if isinstance(op, ast.Eq):
            return left_value == right_value

        elif isinstance(op, ast.NotEq):
            return left_value != right_value

        elif isinstance(op, ast.Lt):
            return left_value < right_value

        elif isinstance(op, ast.LtE):
            return left_value <= right_value

        elif isinstance(op, ast.Gt):
            return left_value > right_value

        elif isinstance(op, ast.GtE):
            return left_value >= right_value

        elif isinstance(op, ast.Is):
            return left_value is right_value

        elif isinstance(op, ast.IsNot):
            return left_value is not right_value

        elif isinstance(op, ast.In):
            return left_value in right_value

        elif isinstance(op, ast.NotIn):
            return left_value not in right_value

        else:
            raise TypeError(f"[compare_expr] {type(op)}는 잘못된 타입입니다.")

    @staticmethod
    def _create_expressions(left_obj, right_obj, op) -> tuple:
        total_expressions = util.transpose_with_last_fill([left_obj.expressions, right_obj.expressions])

        for i in range(len(total_expressions)):
            left_expression = total_expressions[i][0]
            right_expression = total_expressions[i][1]
            total_expressions[i] = list_to_str([left_expression, CompareExpr._get_op_value(op), right_expression])

        return total_expressions

    @staticmethod
    def _create_origin_expression(left_obj: ExprObj, comparators: tuple[ExprObj, ...], ops: tuple[ast.cmpop, ...]):
        expressions = [f"{left_obj.expressions[0]}"]

        for idx, comparator_obj in enumerate(comparators):
            expressions.append(f"{CompareExpr._get_op_to_str(ops[idx])}")
            expressions.append(f"{comparator_obj.expressions[0]}")

        return list_to_str(expressions)

    @staticmethod
    def _get_op_to_str(op: ast.cmpop):
        if isinstance(op, ast.Eq):
            return "=="

        elif isinstance(op, ast.NotEq):
            return "!="

        elif isinstance(op, ast.Lt):
            return "<"

        elif isinstance(op, ast.LtE):
            return "<="

        elif isinstance(op, ast.Gt):
            return ">"

        elif isinstance(op, ast.GtE):
            return ">="

        elif isinstance(op, ast.Is):
            return "is"

        elif isinstance(op, ast.IsNot):
            return "is not"

        elif isinstance(op, ast.In):
            return "in"

        elif isinstance(op, ast.NotIn):
            return "not in"

        else:
            raise TypeError(f"[compare_expr] {type(op)}는 잘못된 타입입니다.")
