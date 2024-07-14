from app.visualize.analysis.stmt.parser.expr.models.expr_obj import ExprObj, AttributeObj


class AttributeExpr:

    @staticmethod
    def parse(target_obj: ExprObj, attr_name: str, arg_objs: list[ExprObj, ...]):
        value = AttributeExpr._get_value(target_obj, attr_name, arg_objs)
        expressions = AttributeExpr._create_expressions(target_obj, value)

        return AttributeObj(value=value, expressions=expressions)

    @staticmethod
    def _get_value(target_obj: ExprObj, attr_name: str, arg_objs: list[ExprObj, ...]):
        target_value = target_obj.value

        getattr(target_value, attr_name)(*[arg.value for arg in arg_objs])

        return target_value

    @staticmethod
    def _create_expressions(target_obj: ExprObj, value):
        return tuple([target_obj.expressions[-1], str(value)])
