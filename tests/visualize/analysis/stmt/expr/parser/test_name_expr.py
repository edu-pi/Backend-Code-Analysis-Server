import ast

import pytest

from app.visualize.analysis.stmt.expr.model.expr_obj import ExprObj, NameObj
from app.visualize.analysis.stmt.expr.parser.name_expr import NameExpr


@pytest.mark.parametrize(
    "ctx, identifier_name, expected",
    [
        (ast.Store(), "a", NameObj(value="a", expressions=("a",))),
        (ast.Store(), "abc", NameObj(value="abc", expressions=("abc",))),
        (ast.Load(), "a", NameObj(value=10, expressions=("a", "10"))),
        (ast.Load(), "abc", NameObj(value=10, expressions=("abc", "10"))),
    ],
)
def test_parse(elem_manager, ctx, identifier_name, expected):
    result = NameExpr.parse(ctx, identifier_name, elem_manager)

    assert result == expected


@pytest.mark.parametrize("identifier, expected", [("a", 10), ("abc", 10)])
def test_get_identifier_value(elem_manager, identifier, expected):
    result = NameExpr._get_identifier_value(identifier, elem_manager)

    assert result == expected


@pytest.mark.parametrize("identifier_name, value, expected", [("a", 10, ("a", "10")), ("abc", 10, ("abc", "10"))])
def test_create_expressions(identifier_name, value, expected):
    result = NameExpr._create_expressions(identifier_name, value)

    assert result == expected
