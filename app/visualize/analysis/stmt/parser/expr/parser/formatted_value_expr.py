from app.visualize.analysis.stmt.parser.expr.models.expr_obj import ExprObj, FormattedValueObj


class FormattedValueExpr:
    @staticmethod
    def parse(expr_obj: ExprObj, conversion, format_spec: ExprObj):
        value = FormattedValueExpr._get_value(expr_obj, conversion, format_spec)
        expressions = FormattedValueExpr._concat_expressions(expr_obj, conversion, format_spec)

        return FormattedValueObj(value, expressions)

    @staticmethod
    def _get_value(expr_obj: ExprObj, conversion, format_spec):
        return expr_obj.value

    @staticmethod
    def _concat_expressions(expr_obj: ExprObj, conversion, format_spec):
        expressions = []

        for idx, expression in enumerate(expr_obj.expressions):
            if idx == len(expr_obj.expressions) - 1:
                expressions.append(expression)
            else:
                expressions.append("{" + expression + "}")

        return tuple(expressions)
