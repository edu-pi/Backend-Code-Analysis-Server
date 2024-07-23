import ast

import pytest

from app.visualize.analysis.stmt.models.flow_control_obj import PassStmtObj
from app.visualize.analysis.stmt.parser.flow_control_stmt import PassStmt


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
def test_parse(node: ast.Pass, expect):
    actual = PassStmt.parse(node)

    assert actual == PassStmtObj(id=node.lineno)
