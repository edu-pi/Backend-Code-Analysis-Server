import ast

import pytest

from app.visualize.analysis.stmt.expr.models.expr_obj import ExprObj, NameObj
from app.visualize.analysis.stmt.expr.parser.name_expr import NameExpr


@pytest.mark.parametrize(
    "ctx, identifier_name, expected",
    [
        pytest.param(ast.Store(), "a", NameObj(value="a", expressions=("a",)), id="a ast.Store(): success case"),
        pytest.param(
            ast.Store(), "abc", NameObj(value="abc", expressions=("abc",)), id="abc ast.Store(): success case"
        ),
        pytest.param(ast.Load(), "a", NameObj(value=10, expressions=("a", "10")), id="a ast.Load(): success case"),
        pytest.param(
            ast.Load(), "abc", NameObj(value=10, expressions=("abc", "10")), id="abc ast.Load(): success case"
        ),
    ],
)
def test_parse(elem_manager, ctx, identifier_name, expected):
    result = NameExpr.parse(ctx, identifier_name, elem_manager)

    assert result == expected


@pytest.mark.parametrize(
    "identifier, expected",
    [pytest.param("a", 10, id="a: success case"), pytest.param("abc", 10, id="abc: success case")],
)
def test_get_identifier_value(elem_manager, identifier, expected):
    result = NameExpr._get_identifier_value(identifier, elem_manager)

    assert result == expected


@pytest.mark.parametrize(
    "identifier_name, value, expected",
    [
        pytest.param("a", 10, ("a", "10"), id="a 10: success case"),
        pytest.param("abc", 10, ("abc", "10"), id="abc 10: success case"),
        pytest.param("b", "Hello", ("b", "'Hello'"), id="b Hello: success case"),
    ],
)
def test_create_expressions(identifier_name, value, expected):
    result = NameExpr._create_expressions(identifier_name, value)

    assert result == expected
