
from app.visualize.analysis.stmt.parser.expr.models.expr_obj import (
    ExprObj,
    SliceObj,
    SubscriptObj,
)


class SubscriptExpr:

    @staticmethod
    def parse(target_obj: ExprObj, slice_obj: ExprObj) -> SubscriptObj:
        value = SubscriptExpr._get_value(target_obj.value, slice_obj.value)
        expressions = SubscriptExpr._create_expressions(target_obj, slice_obj)

        return SubscriptObj(value=value, expressions=expressions)

    @staticmethod
    def _get_value(target_obj_value: list, slice_obj_value: slice | int):
        return target_obj_value[slice_obj_value]

    @staticmethod
    def _create_expressions(target_obj: ExprObj, slice_obj: ExprObj):
        subscript_value = SubscriptExpr._get_value(target_obj.value, slice_obj.value)
        subscript_expressions = []
        format_string = SubscriptExpr._get_subscript_format_string(slice_obj)
        target_name = target_obj.expressions[0]

        for slice_obj_expression in slice_obj.expressions:
            subscript_expressions.append(format_string.format(target_name, slice_obj_expression))

        subscript_expressions.append(str(subscript_value))

        return tuple(subscript_expressions)

    @staticmethod
    def _get_subscript_format_string(slice_obj: ExprObj):
        if isinstance(slice_obj, SliceObj):
            return "{}{}"

        return "{}[{}]"
