import ast

from app.visualize.analysis.stmt.models.flow_control_obj import (
    BreakStmtObj,
    PassStmtObj,
    ContinueStmtObj,
    ReturnStmtObj,
)
from app.visualize.analysis.stmt.parser.expr.expr_traveler import ExprTraveler
from app.visualize.container.element_container import ElementContainer


class BreakStmt:
    @staticmethod
    def parse(node: ast.Break) -> BreakStmtObj:
        return BreakStmtObj(id=node.lineno)


class PassStmt:
    @staticmethod
    def parse(node: ast.Pass) -> PassStmtObj:
        return PassStmtObj(id=node.lineno)


class ContinueStmt:
    @staticmethod
    def parse(node: ast.Continue) -> ContinueStmtObj:
        return ContinueStmtObj(id=node.lineno)


class ReturnStmt:
    @staticmethod
    def parse(node: ast.Return, elem_container: ElementContainer) -> ReturnStmtObj:
        return_value_obj = ExprTraveler.travel(node.value, elem_container)
        return ReturnStmtObj(id=node.lineno, value=return_value_obj.value, expr=return_value_obj.expressions)
