import ast

import pytest

from app.visualize.analysis.stmt.parser.expr.models.expr_obj import NameObj
from app.visualize.analysis.stmt.parser.expr.parser.name_expr import NameExpr


@pytest.mark.parametrize(
    "ctx, identifier_name, value, expressions",
    [
        pytest.param(ast.Store(), "a", "a", ("a",), id="a ast.Store(): success case"),
        pytest.param(ast.Store(), "abc", "abc", ("abc",), id="abc ast.Store(): success case"),
        pytest.param(ast.Load(), "a", 10, ("a", "10"), id="a ast.Load(): success case"),
        pytest.param(ast.Load(), "abc", 10, ("abc", "10"), id="abc ast.Load(): success case"),
    ],
)
def test_parse(elem_container, mocker, ctx, identifier_name, value, expressions):
    mocker.patch(
        "app.visualize.analysis.stmt.parser.expr.parser.name_expr.NameExpr._get_identifier_value", return_value=value
    )
    mocker.patch(
        "app.visualize.analysis.stmt.parser.expr.parser.name_expr.NameExpr._create_expressions",
        return_value=expressions,
    )
    result = NameExpr.parse(ctx, identifier_name, elem_container)

    assert isinstance(result, NameObj)
    assert result.value == value
    assert result.expressions == expressions


def test_parse_fail_ast_del(elem_container, mocker):
    ast_del = mocker.MagicMock(spec=ast.Del)

    with pytest.raises(NotImplementedError):
        NameExpr.parse(ast_del, "a", elem_container)


@pytest.mark.parametrize(
    "identifier, expected",
    [pytest.param("a", 10, id="a: success case"), pytest.param("abc", 10, id="abc: success case")],
)
def test_get_identifier_value(elem_container, identifier, expected):
    result = NameExpr._get_identifier_value(identifier, elem_container)

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
