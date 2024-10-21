import ast

from app.visualize.analysis.stmt.parser.expr.models.expr_obj import ArgumentsObj


class ArgumentsExpr:

    @staticmethod
    def parse(node: ast.arguments) -> ArgumentsObj:
        value = ArgumentsExpr._get_value(node)
        expressions = ArgumentsExpr._create_expressions(node)
        return ArgumentsObj(value=value, expressions=expressions)

    @staticmethod
    def _get_value(node: ast.arguments):
        return tuple(argument.arg for argument in node.args)

    @staticmethod
    def _create_expressions(node: ast.arguments) -> tuple:
        return tuple(argument.arg for argument in node.args)
