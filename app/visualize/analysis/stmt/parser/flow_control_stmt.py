import ast

from app.visualize.analysis.stmt.models.flow_control_obj import BreakStmtObj, PassStmtObj


class BreakStmt:
    @staticmethod
    def parse(node: ast.Break) -> BreakStmtObj:
        return BreakStmtObj(id=node.lineno, expr="break")


class PassStmt:
    @staticmethod
    def parse(node: ast.Pass) -> PassStmtObj:
        return PassStmtObj(id=node.lineno, expr="pass")
