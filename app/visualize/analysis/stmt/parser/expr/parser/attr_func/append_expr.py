from app.visualize.analysis.stmt.parser.expr.models.expr_obj import AttributeObj, ExprObj


class AppendExpr:

    @staticmethod
    def parse(attr_obj: AttributeObj, args: list[ExprObj]):
        AppendExpr._append_value(attr_obj, args)
        value = AppendExpr._get_value(attr_obj)
        expressions = AppendExpr._create_expressions(args)

        return AttributeObj(value=value, expressions=expressions, type="append")

    @staticmethod
    def _append_value(attr_obj: AttributeObj, args: list[ExprObj]):
        append_method = attr_obj.value

        append_method(*args)

    @staticmethod
    def _get_value(attr_obj: AttributeObj):
        return attr_obj.expressions[0]

    @staticmethod
    def _create_expressions(args: list[ExprObj]):

        return args[0].expressions
