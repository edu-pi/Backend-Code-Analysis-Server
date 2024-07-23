import ast

from app.visualize.analysis.stmt.models.flow_control_obj import BreakStmtObj, PassStmtObj
from app.visualize.analysis.stmt.models.stmt_type import StmtType


class BreakStmt:
    @staticmethod
    def parse(node: ast.Break) -> BreakStmtObj:
        return BreakStmtObj(id=node.lineno)


class PassStmt:
    @staticmethod
    def parse(node: ast.Pass) -> PassStmtObj:
        return PassStmtObj(id=node.lineno)
