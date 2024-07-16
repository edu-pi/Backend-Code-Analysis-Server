from app.visualize.analysis.stmt.parser.expr.models.expr_obj import AttributeObj, ExprObj, AppendObj


class AppendExpr:

    @staticmethod
    def parse(attr_obj: AttributeObj, args: list[ExprObj]):
        if len(args) != 1:
            raise ValueError(
                f"[AppendExpr] append() 함수는 1개의 인자만 받을 수 있습니다. ({len(args)}개의 인자가 입력됨)"
            )

        AppendExpr._append_value(attr_obj, args[0])
        value = AppendExpr._get_value(attr_obj)
        expressions = AppendExpr._create_expressions(args[0])

        return AppendObj(value=value, expressions=expressions)

    @staticmethod
    def _append_value(attr_obj: AttributeObj, arg: ExprObj):
        append_method = attr_obj.value

        append_method(arg.value)

    @staticmethod
    def _get_value(attr_obj: AttributeObj):
        return attr_obj.expressions[0]

    @staticmethod
    def _create_expressions(arg: ExprObj):
        return arg.expressions
