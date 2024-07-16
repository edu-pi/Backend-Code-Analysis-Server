from app.visualize.analysis.stmt.parser.expr.models.expr_obj import ExprObj, RangeObj
from app.visualize.analysis.stmt.parser.expr.models.range_expression import RangeExpression
from app.visualize.utils import utils


class RangeExpr:

    @staticmethod
    def parse(args: list[ExprObj]):
        value = RangeExpr._get_value([arg.value for arg in args])
        expressions = RangeExpr._create_expressions([arg.expressions for arg in args])

        return RangeObj(value=value, expressions=expressions)

    @staticmethod
    def _get_value(arg_value_list: list):
        start = 0
        step = 1

        if len(arg_value_list) == 1:
            end = arg_value_list[0]

        elif len(arg_value_list) == 2:
            start = arg_value_list[0]
            end = arg_value_list[1]

        elif len(arg_value_list) == 3:
            start = arg_value_list[0]
            end = arg_value_list[1]
            step = arg_value_list[2]

        else:
            raise TypeError(f"[CallParser]: {arg_value_list} 인자의 개수가 잘못되었습니다.")

        return tuple(range(int(start), int(end), int(step)))

    @staticmethod
    def _create_expressions(args_expressions: list[tuple]):

        # utils의 transpose_with_last_fill을 이용하여 값 배열 생성
        # ['a', '10', '2'], ['3', '10', '2']
        transposed_expressions = utils.transpose_with_last_fill(args_expressions)

        # 배열을 range_obj로 만들기
        range_expressions = [RangeExpr._make_unit_range_expression(range_list) for range_list in transposed_expressions]

        return tuple(range_expressions)

    @staticmethod
    def _make_unit_range_expression(range_list: list):
        if len(range_list) == 1:
            return RangeExpression(start="0", end=str(range_list[0]), step="1")

        elif len(range_list) == 2:
            return RangeExpression(start=str(range_list[0]), end=str(range_list[1]), step="1")

        elif len(range_list) == 3:
            return RangeExpression(start=str(range_list[0]), end=str(range_list[1]), step=str(range_list[2]))

        else:
            raise TypeError(f"[CallParser]: {range_list} 인자의 개수가 잘못되었습니다.")
