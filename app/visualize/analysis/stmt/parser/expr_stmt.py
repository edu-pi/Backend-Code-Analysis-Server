import ast

from app.visualize.analysis.stmt.models.expr_stmt_obj import ExprStmtObj
from app.visualize.analysis.stmt.parser.expr.expr_traveler import ExprTraveler
from app.visualize.container.element_container import ElementContainer


class ExprStmt:

    @staticmethod
    def parse(node: ast.Expr, elem_container: ElementContainer):
        expr_obj = ExprStmt._get_expr_obj(node.value, elem_container)
        return ExprStmtObj(
            id=node.lineno,
            value=expr_obj.value,
            expressions=expr_obj.expressions,
            expr_type=expr_obj.type,
            call_stack_name=elem_container.get_call_stack_name(),
        )

    @staticmethod
    def _get_expr_obj(node: ast, elem_container: ElementContainer):
        return ExprTraveler.travel(node, elem_container)
