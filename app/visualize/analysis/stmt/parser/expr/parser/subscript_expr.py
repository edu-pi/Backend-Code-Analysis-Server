import ast

from app.visualize.analysis.stmt.parser.expr.models.expr_obj import (
    ExprObj,
    SliceObj,
    SubscriptObj,
)
from app.visualize.analysis.stmt.parser.expr.models.expr_type import ExprType


class SubscriptExpr:

    @staticmethod
    def parse(target_obj: ExprObj, slice_obj: ExprObj, ctx: ast) -> SubscriptObj:
        if isinstance(ctx, ast.Load):
            value = SubscriptExpr._get_value(target_obj, slice_obj, ctx)
            expressions = SubscriptExpr._create_expressions(target_obj, slice_obj, value)

        elif isinstance(ctx, ast.Store):
            value = SubscriptExpr._get_value(target_obj, slice_obj, ctx)
            expressions = (value,)

        else:
            raise TypeError(f"[StmtTraveler] {type(ctx)}는 지원하지 않는 타입입니다.")

        return SubscriptObj(value=value, expressions=expressions, type=ExprType.judge_collection_type(value))

    @staticmethod
    def _get_value(target_obj_value: ExprObj, slice_obj_value: ExprObj, ctx: ast):
        if isinstance(ctx, ast.Load):
            return target_obj_value.value[slice_obj_value.value]

        elif isinstance(ctx, ast.Store):
            if slice_obj_value.type is ExprType.SLICE:
                return target_obj_value.expressions[0] + str(slice_obj_value.expressions[-1])
            else:
                return target_obj_value.expressions[0] + "[" + str(slice_obj_value.expressions[-1]) + "]"

    @staticmethod
    def _create_expressions(target_obj: ExprObj, slice_obj: ExprObj, subscript_value):
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
