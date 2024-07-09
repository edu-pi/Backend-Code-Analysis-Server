import ast

from app.visualize.container.element_container import ElementContainer
from app.visualize.analysis.stmt.parser.expr.expr_traveler import ExprTraveler
from app.visualize.analysis.stmt.models.expr_stmt_obj import ExprStmtObj


class ExprStmt:

    @staticmethod
    def parse(node: ast.Expr, elem_container: ElementContainer):
        expr_obj = ExprStmt._get_expr_obj(node.value, elem_container)
        return ExprStmtObj(
            id=node.lineno, value=expr_obj.value, expressions=expr_obj.expressions, expr_type=expr_obj.type
        )

    @staticmethod
    def _get_expr_obj(node: ast, elem_container: ElementContainer):
        return ExprTraveler.travel(node, elem_container)
