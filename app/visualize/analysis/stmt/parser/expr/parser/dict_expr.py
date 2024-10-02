import json

from app.visualize.analysis.stmt.parser.expr.models.expr_obj import ExprObj, DictObj


class DictExpr:

    @staticmethod
    def parse(keys: list[ExprObj], values: list[ExprObj]):
        value = DictExpr._get_value(keys, values)
        expressions = DictExpr._concat_expressions(value)

        return DictObj(value=value, expressions=expressions)

    @staticmethod
    def _get_value(keys: list[ExprObj], values: list[ExprObj]):
        dictionary = {}

        for i in range(len(keys)):
            key = keys[i].value
            value = values[i].value
            dictionary[key] = value

        return dictionary

    @staticmethod
    def _concat_expressions(value: dict):
        expr = json.dumps(value)
        return (expr,)
