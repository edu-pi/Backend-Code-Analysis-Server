import ast

import pytest

from app.visualize.analysis.stmt.models.flow_control_obj import PassStmtObj, ContinueStmtObj, BreakStmtObj
from app.visualize.analysis.stmt.models.stmt_type import StmtType
from app.visualize.analysis.stmt.parser.flow_control_stmt import PassStmt, ContinueStmt, BreakStmt


@pytest.mark.parametrize(
    "node, expect",
    [
        pytest.param(
            ast.Break(lineno=1),
            BreakStmtObj(id=1),
            id="pass: success case",
        ),
    ],
)
def test_break_parse(node: ast.Break, expect):
    actual = BreakStmt.parse(node)

    assert actual == expect
    assert actual.flow_control_type is StmtType.BREAK
    assert actual.type is StmtType.FLOW_CONTROL


@pytest.mark.parametrize(
    "node, expect",
    [
        pytest.param(
            ast.Pass(lineno=1),
            PassStmtObj(id=1),
            id="pass: success case",
        ),
    ],
)
def test_pass_parse(node: ast.Pass, expect):
    actual = PassStmt.parse(node)

    assert actual == expect
    assert actual.flow_control_type is StmtType.PASS
    assert actual.type is StmtType.FLOW_CONTROL


@pytest.mark.parametrize(
    "node, expect",
    [
        pytest.param(
            ast.Continue(lineno=1),
            ContinueStmtObj(id=1),
            id="continue: success case",
        ),
    ],
)
def test_continue_parse(node: ast.Continue, expect):
    actual = ContinueStmt.parse(node)

    assert actual == expect
    assert actual.flow_control_type is StmtType.CONTINUE
    assert actual.type is StmtType.FLOW_CONTROL
