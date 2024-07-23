import ast

from app.visualize.analysis.stmt.models.flow_control_obj import BreakStmtObj, PassStmtObj, ContinueStmtObj
from app.visualize.analysis.stmt.models.stmt_type import StmtType


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
