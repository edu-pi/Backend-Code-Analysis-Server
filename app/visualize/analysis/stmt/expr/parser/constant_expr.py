import ast

from app.visualize.analysis.stmt.expr.model.expr_obj import ExprObj


class ConstantExpr:
    @staticmethod
    def parse(node: ast.Constant):
        value = ConstantExpr._get_literal(node)
        expressions = ConstantExpr._create_expressions(value)
        return ExprObj(type="constant", value=value, expressions=expressions)

    @staticmethod
    def _get_literal(node: ast.Constant):
        return node.value

    @staticmethod
    def _create_expressions(value):
        return [str(value)]