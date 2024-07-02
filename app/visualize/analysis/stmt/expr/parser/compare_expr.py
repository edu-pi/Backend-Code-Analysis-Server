import ast

from app.visualize.analysis.stmt.expr.model.expr_obj import ExprObj


class CompareExpr:

    @staticmethod
    def parse(left_obj: ExprObj, comparators: tuple[ExprObj, ...], op: tuple[ast.cmpop, ...]):
        value = CompareExpr._get_final_calculate_value(left_obj, comparators, op)
        print("+++++++++++++: ", value)

    @staticmethod
    def _get_final_calculate_value(left_obj: ExprObj, comparators: tuple[ExprObj, ...], ops: tuple[ast.cmpop, ...]):
        left = left_obj.value
        # 피연자 값과 비교 연산자를 순차적으로 계산
        for idx, comparator_obj in enumerate(comparators):
            right = comparator_obj.value
            if not CompareExpr._calculate_value(left, right, ops[idx]):
                return False
            left = right
        return True

    @staticmethod
    def _calculate_value(left_value, right_value, op: ast):
        if isinstance(op, ast.Eq):
            return left_value == right_value

        elif isinstance(op, ast.NotEq):
            return left_value != right_value

        elif isinstance(op, ast.Lt):
            return left_value < right_value

        elif isinstance(op, ast.LtE):  # '/'
            return left_value <= right_value  # 실수로 계산

        elif isinstance(op, ast.Gt):  # '//'
            return left_value > right_value  # 정수로 계산

        elif isinstance(op, ast.GtE):  # '//'
            return left_value >= right_value  # 정수로 계산

        elif isinstance(op, ast.Is):  # '//'
            return left_value is right_value  # 정수로 계산

        elif isinstance(op, ast.IsNot):  # '//'
            return left_value is not right_value  # 정수로 계산

        elif isinstance(op, ast.In):  # '//'
            return left_value in right_value  # 정수로 계산

        elif isinstance(op, ast.NotIn):  # '//'
            return left_value not in right_value  # 정수로 계산

        else:
            raise TypeError(f"[compare_expr] {type(op)}는 잘못된 타입입니다.")
