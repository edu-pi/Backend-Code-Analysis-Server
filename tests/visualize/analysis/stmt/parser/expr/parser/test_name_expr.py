import ast

import pytest

from app.visualize.analysis.stmt.parser.expr.models.expr_obj import NameObj
from app.visualize.analysis.stmt.parser.expr.parser.name_expr import NameExpr


@pytest.mark.parametrize(
    "node, expected",
    [
        pytest.param(
            ast.Name(ctx=ast.Store(), id="a"), NameObj(value="a", expressions=("a",)), id="a ast.Store(): success case"
        ),
        pytest.param(
            ast.Name(ctx=ast.Store(), id="abc"),
            NameObj(value="a", expressions=("a",)),
            id="abc ast.Store(): success case",
        ),
        pytest.param(
            ast.Name(ctx=ast.Load(), id="a"),
            NameObj(value=10, expressions=("a", "10")),
            id="a ast.Load(): success case",
        ),
        pytest.param(
            ast.Name(ctx=ast.Load(), id="a"),
            NameObj(value=10, expressions=("a", "10")),
            id="abc ast.Load(): success case",
        ),
    ],
)
def test_parse(elem_container, mocker, node: ast.Name, expected: NameObj):
    mock_get_identifier_value = mocker.patch.object(NameExpr, "_get_identifier_value", return_value=expected.value)
    mock_create_expressions = mocker.patch.object(NameExpr, "_create_expressions", return_value=expected.expressions)
    result = NameExpr.parse(node, elem_container)

    assert isinstance(result, NameObj)
    assert mock_get_identifier_value.call_once_with(node.id, elem_container)
    assert mock_create_expressions.call_once_with(node.id, expected.value)


def test_parse_fail_ast_del(elem_container, mocker):
    ast_name_ctx_del = mocker.MagicMock(spec=ast.Name, ctx=ast.Del())

    with pytest.raises(NotImplementedError):
        NameExpr.parse(ast_name_ctx_del, elem_container)


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
