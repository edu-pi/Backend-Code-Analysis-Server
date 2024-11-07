import ast

from app.visualize.analysis.stmt.parser.expr.models.expr_obj import ExprObj, ConstantObj


class UnaryOpExpr:
    # Invert(~1), Not(not 1), UAdd(+1), USub(-1)
    @staticmethod
    def parse(op: ast, operand: ExprObj):
        value = UnaryOpExpr._get_value(op, operand)
        expressions = UnaryOpExpr._concat_expressions(op, operand)
        return ConstantObj(value=value, expressions=expressions)

    @staticmethod
    def _get_value(op: ast, operand: ExprObj):
        if isinstance(op, ast.Invert):
            return ~operand.value
        elif isinstance(op, ast.Not):
            return not operand.value
        elif isinstance(op, ast.UAdd):
            return +operand.value
        elif isinstance(op, ast.USub):
            return -operand.value

    @staticmethod
    def _concat_expressions(op: ast, operand: ExprObj):
        expressions = []

        for expression in operand.expressions:
            if isinstance(op, ast.Invert):
                expressions.append(f"~{expression}")
            elif isinstance(op, ast.Not):
                expressions.append(f"not {expression}")
            elif isinstance(op, ast.UAdd):
                expressions.append(f"+{expression}")
            elif isinstance(op, ast.USub):
                expressions.append(f"-{expression}")
        return tuple(expressions)
