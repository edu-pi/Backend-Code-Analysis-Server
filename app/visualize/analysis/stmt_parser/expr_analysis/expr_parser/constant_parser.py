import ast
from dataclasses import dataclass

from app.visualize.analysis.stmt_parser.expr_analysis.expr_models.expr_obj import ExprObj


class ConstantParser:
    @staticmethod
    def parse(node: ast.Constant):
        value = ConstantParser._get_literal(node)
        expressions = ConstantParser._create_expressions(value)
        return ExprObj(value=value, expressions=expressions)

    @staticmethod
    def _get_literal(node: ast.Constant):
        return node.value

    @staticmethod
    def _create_expressions(value):
        return [str(value)]
