import ast

import pytest

from app.visualize.analysis.stmt.parser.expr.models.expr_obj import ConstantObj
from app.visualize.analysis.stmt.parser.expr.parser.constant_expr import ConstantExpr


@pytest.mark.parametrize(
    "mock_value, expected",
    [
        pytest.param(10, ConstantObj(value=10, expressions=("10",)), id="10: success case"),
        pytest.param("Hello", ConstantObj(value="Hello", expressions=("'Hello'",)), id="'Hello': success case"),
        pytest.param("World", ConstantObj(value="World", expressions=("'World'",)), id="'World': success case"),
    ],
)
def test_parse(mocker, mock_value, expected):
    mocker.patch(
        "app.visualize.analysis.stmt.parser.expr.parser.constant_expr.ConstantExpr._get_literal",
        return_value=mock_value,
    )
    result = ConstantExpr.parse(mocker.MagicMock(spec=ast.Constant))

    assert result == expected


@pytest.mark.parametrize(
    "node, expected",
    [
        pytest.param(ast.Constant(value=10), 10, id="10: success case"),
        pytest.param(ast.Constant(value="Hello"), "Hello", id="'Hello': success case"),
        pytest.param(ast.Constant(value="World"), "World", id="'World': success case"),
    ],
)
def test_get_literal(node: ast.Constant, expected):
    result = ConstantExpr._get_literal(node)

    assert result == expected


@pytest.mark.parametrize(
    "value, expected",
    [
        pytest.param(10, ("10",), id="10: success case"),
        pytest.param("Hello", ("'Hello'",), id="'Hello': success case"),
        pytest.param("World", ("'World'",), id="'World': success case"),
    ],
)
def test_create_expressions(value, expected):
    result = ConstantExpr._create_expressions(value)

    assert result == expected
