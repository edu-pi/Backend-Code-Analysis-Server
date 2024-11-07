from app.visualize.analysis.stmt.parser.expr.models.expr_obj import ExprObj, LenObj


class LenExpr:

    @staticmethod
    def parse(args: list[ExprObj]):
        value = LenExpr._get_value(args)
        expressions = LenExpr._create_expressions(args, value)

        return LenObj(value=value, expressions=expressions)

    @staticmethod
    def _get_value(args):
        return str(len(args[0].value))

    @staticmethod
    def _create_expressions(args: list[ExprObj], value):
        expressions = []
        if args:
            expressions.append(f"len({args[0].value})")
        else:
            expressions.append("len()")

        expressions.append(value)
        return tuple(expressions)
