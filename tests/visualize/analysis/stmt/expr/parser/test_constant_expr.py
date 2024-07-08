import ast

import pytest

from app.visualize.analysis.stmt.expr.model.expr_obj import ConstantObj
from app.visualize.analysis.stmt.expr.parser.constant_expr import ConstantExpr


@pytest.mark.parametrize(
    "node, expected",
    [
        pytest.param(ast.Constant(value=10), ConstantObj(value=10, expressions=("10",)), id="10: success case"),
        pytest.param(
            ast.Constant(value="abc"), ConstantObj(value="abc", expressions=("'abc'",)), id="'abc': success case"
        ),
    ],
)
def test_parse(node: ast.Constant, expected):
    result = ConstantExpr.parse(node)

    assert result == expected


@pytest.mark.parametrize(
    "node, expected",
    [
        pytest.param(ast.Constant(value=10), 10),
        pytest.param(ast.Constant(value="abc"), "abc", id="'abc': success case"),
    ],
)
def test_get_literal(node: ast.Constant, expected):
    result = ConstantExpr._get_literal(node)

    assert result == expected


@pytest.mark.parametrize(
    "value, expected",
    [pytest.param(10, ("10",), id="10: success case"), pytest.param("abc", ("'abc'",), id="'abc': success case")],
)
def test_create_expressions(value, expected):
    result = ConstantExpr._create_expressions(value)

    assert result == expected
