import ast

from app.visualize.analysis.stmt.models.flowcontrolobj.pass_stmt_obj import PassStmtObj


class PassStmt:
    @staticmethod
    def parse(node: ast.Pass) -> PassStmtObj:
        return PassStmtObj(id=node.lineno, expr="pass")
