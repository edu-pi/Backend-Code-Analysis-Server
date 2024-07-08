import ast

from app.visualize.analysis.element_manager import CodeElementManager
from app.visualize.analysis.stmt.expr.expr_traveler import ExprTraveler
from app.visualize.analysis.stmt.models.expr_stmt_obj import ExprStmtObj


class ExprStmt:

    @staticmethod
    def parse(node: ast.Expr, elem_manager: CodeElementManager):
        expr_obj = ExprStmt._get_expr_obj(node.value, elem_manager)
        return ExprStmtObj(
            id=node.lineno, value=expr_obj.value, expressions=expr_obj.expressions, expr_type=expr_obj.type
        )

    @staticmethod
    def _get_expr_obj(node: ast, elem_manager: CodeElementManager):
        return ExprTraveler.travel(node, elem_manager)
