import ast

from app.visualize.analysis.stmt.models.flow_control_obj import BreakStmtObj
from app.visualize.analysis.stmt.parser.flow_control_stmt import BreakStmt


def test_parse():
    node = ast.Break(lineno=1)

    actual = BreakStmt.parse(node)

    assert actual == BreakStmtObj(id=1, expr="break")
