import ast

import pytest

from app.visualize.analysis.stmt.models.pass_stmt_obj import PassStmtObj
from app.visualize.analysis.stmt.parser.pass_stmt import PassStmt


@pytest.mark.parametrize(
    "node, expect",
    [
        pytest.param(
            ast.Pass(lineno=1),
            PassStmtObj(id=1, expr="pass"),
            id="pass: success case",
        ),
    ],
)
def test_parse(node: ast.Pass, expect):
    actual = PassStmt.parse(node)

    assert actual == PassStmtObj(id=node.lineno, expr="pass")
