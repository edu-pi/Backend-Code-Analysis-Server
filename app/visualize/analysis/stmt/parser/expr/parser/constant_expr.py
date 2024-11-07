import ast

from app.visualize.analysis.stmt.parser.expr.models.expr_obj import ConstantObj


class ConstantExpr:
    @staticmethod
    def parse(node: ast.Constant):
        value = ConstantExpr._get_literal(node)
        expressions = ConstantExpr._create_expressions(value)
        return ConstantObj(value=value, expressions=expressions)

    @staticmethod
    def _get_literal(node: ast.Constant):
        return node.value

    @staticmethod
    def _create_expressions(value) -> tuple:
        if isinstance(value, str):
            return (f"'{value}'",)
        return (str(value),)
