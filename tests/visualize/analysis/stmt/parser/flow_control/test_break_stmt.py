import ast

from app.visualize.analysis.stmt.models.flowcontrolobj.break_stmt_obj import BreakStmtObj
from app.visualize.analysis.stmt.parser.flowcontrol.break_stmt import BreakStmt


def test_parse():
    node = ast.Break(lineno=1)

    actual = BreakStmt.parse(node)

    assert actual == BreakStmtObj(id=1, expr="break")
