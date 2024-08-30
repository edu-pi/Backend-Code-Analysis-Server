from app.visualize.analysis.stmt.parser.expr.models.expr_obj import ExprObj, ConstantObj
from app.visualize.utils import utils


class JoinedStrExpr:
    @staticmethod
    def parse(value_objs: list[ExprObj]):
        value = JoinedStrExpr._get_value(value_objs)
        expressions = JoinedStrExpr._concat_expressions(value_objs, value)

        return ConstantObj(value=value, expressions=expressions)

    @staticmethod
    def _get_value(value_objs: list[ExprObj]):
        return "".join(str(value_obj.value) for value_obj in value_objs)

    @staticmethod
    def _concat_expressions(value_objs: list[ExprObj], value):
        expressions = []

        transposed_expressions = utils.transpose_with_last_fill([value_obj.expressions for value_obj in value_objs])

        for transposed_expression in transposed_expressions:
            without_apostrophe = [
                expression[1:-1] if str(expression).startswith("'") and expression.endswith("'") else expression
                for expression in transposed_expression
            ]

            expressions.append("".join(without_apostrophe))

        transposed_expressions.append(value)

        return tuple(expressions)
