import ast

from app.visualize.analysis.stmt.models.flowcontrolobj.break_stmt_obj import BreakStmtObj


class BreakStmt:
    @staticmethod
    def parse(node: ast.Break) -> BreakStmtObj:
        return BreakStmtObj(id=node.lineno, expr="break")
