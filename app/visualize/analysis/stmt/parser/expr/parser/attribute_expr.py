from app.visualize.analysis.stmt.parser.expr.models.expr_obj import ExprObj, AttributeObj


class AttributeExpr:

    @staticmethod
    def parse(target_obj: ExprObj, attr_name: str):
        value = AttributeExpr._get_value(target_obj, attr_name)
        expressions = AttributeExpr._create_expressions(target_obj)

        return AttributeObj(value=value, expressions=expressions, type=attr_name)

    @staticmethod
    def _get_value(target_obj: ExprObj, attr_name: str):
        target_value = target_obj.value

        return getattr(target_value, attr_name)

    @staticmethod
    def _create_expressions(target_obj: ExprObj):
        return target_obj.expressions
