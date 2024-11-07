import ast

from app.visualize.analysis.stmt.models.return_stmt_obj import ReturnStmtObj
from app.visualize.analysis.stmt.parser.expr.expr_traveler import ExprTraveler
from app.visualize.container.element_container import ElementContainer


class ReturnStmt:
    @staticmethod
    def parse(node: ast.Return, elem_container: ElementContainer) -> ReturnStmtObj:
        if node.value is None:
            return ReturnStmtObj(id=node.lineno, value=None, expr=("",))
        return_value_obj = ExprTraveler.travel(node.value, elem_container)
        return ReturnStmtObj(id=node.lineno, value=return_value_obj.value, expr=return_value_obj.expressions)
