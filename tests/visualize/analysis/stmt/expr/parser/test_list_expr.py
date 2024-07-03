import ast

import pytest


@pytest.fixture
def create_list():
    def _create_list_ast(elts, ctx):
        return ast.List(elts=elts, ctx=ctx)

    return _create_list_ast


@pytest.mark.parametrize(
    "elts, ctx, expected",
    [
        pytest.param(
            [ast.Constant(value=10), ast.Constant(value=20)],
            ast.Load(),
            ListObj(value=(10, 20), expressions=("[10, 20]",)),
            id="[10, 20] 배열이 들어오는 경우 - Load",
        ),
        pytest.param(
            [
                ast.BinOp(left=ast.Name("a", ast.Load()), op=ast.Add(), right=ast.Constant(value=1)),
                ast.Constant(value=20),
            ],
            ast.Load(),
            ListObj(value=(11, 20), expressions=("[a + 1, 20]", "[10 + 1, 20]", "[11, 20]")),
            id="[a + 1, 20] 배열이 들어오는 경우 - Load",
        ),
        pytest.param(
            [ast.Constant(value="Hello"), ast.Constant(value="World")],
            ast.Load(),
            ListObj(value=("Hello", "World"), expressions=('["Hello", "World"]',)),
            id='["Hello", "World"] 배열이 들어오는 경우 - Load',
        ),
        pytest.param(
            [ast.Name(id="a", ctx=ast.Store()), ast.Name(id="b", ctx=ast.Store())],
            ast.Store(),
            ListObj(value=["a", "b"], expressions=('["a", "b"]',)),
            id="[a, b] 배열이 들어오는 경우 - Store",
        ),
    ],
)
def test_parse(create_list, elem_manager, elts, ctx, expected):
    list_ast = create_list(elts, ctx)
    result = ListExpr.parse(list_ast, elem_manager)

    assert result == expected
