import ast
from unittest.mock import MagicMock, patch

import pytest

from app.analysis.element_manager import CodeElementManager
from app.analysis.generator.parser.tuple_parser import TupleParser, Tuple


@pytest.fixture
def elem_manager():
    mock = MagicMock(spec=CodeElementManager)
    mock.get_variable_value.return_value = 10
    return mock


@pytest.fixture
def create_ast_tuple():
    def _create_ast_tuple(ctx, elts):
        return ast.Tuple(ctx=ctx, elts=elts)

    return _create_ast_tuple


@pytest.mark.parametrize("ctx, elts, expect_value, expect_expressions, expect_result", [
    (  # (a, b)
            ast.Store(),
            [
                ast.Name(id="a", ctx=ast.Store()),
                ast.Name(id="b", ctx=ast.Store())
            ],
            ["a", "b"],
            None,
            Tuple(target_names=("a", "b"), value=None, expressions=None)
    ),
    (  # (a, 5)
            ast.Load(),
            [
                ast.Name(id="a", ctx=ast.Load()),
                ast.Constant(value=5),
                ast.BinOp(left=ast.Name(id="a", ctx=ast.Load()), op=ast.Add(), right=ast.Constant(value=4))
            ],
            None,
            {
                "value": (10, 5, 14),
                "expressions": [("a", "5", "a + 4"), ("10", "5", "10 + 4"), ("10", "5", "14")]
            },
            Tuple(target_names=None, value=(10, 5, 14),
                  expressions=[("a", "5", "a + 4"), ("10", "5", "10 + 4"), ("10", "5", "14")])
    )
])
def test_parse(create_ast_tuple, elem_manager, ctx, elts, expect_value, expect_expressions, expect_result):
    with patch.object(TupleParser, '_TupleParser__get_target_names', return_value=expect_value), \
            patch.object(TupleParser, '_TupleParser__calculate_node', return_value=expect_expressions):
        result = TupleParser.parse(create_ast_tuple(ctx=ctx, elts=elts), elem_manager)

    assert result == expect_result


@pytest.mark.parametrize("ctx, elts, expect_result", [
    (  # (a, b)
            ast.Store(),
            [
                ast.Name(id="a", ctx=ast.Store()),
                ast.Name(id="b", ctx=ast.Store())
            ],
            ["a", "b"]
    ),
    (  # (abc, def, ghj)
            ast.Store(),
            [
                ast.Name(id="abc", ctx=ast.Store()),
                ast.Name(id="def", ctx=ast.Store()),
                ast.Name(id="ghj", ctx=ast.Store())
            ],
            ["abc", "def", "ghj"]
    )
])
def test__get_target_names(create_ast_tuple, elem_manager, ctx, elts, expect_result):
    ast_tuple = create_ast_tuple(ctx=ctx, elts=elts)
    tuple_parser = TupleParser(ast_tuple, elem_manager)

    result = tuple_parser._TupleParser__get_target_names()

    assert result == expect_result


@pytest.mark.parametrize("ctx, elts, expect_result", [
    (  # (a, 5)
            ast.Load(),
            [
                ast.Name(id="a", ctx=ast.Load()),
                ast.Constant(value=5),
            ],
            {
                "value": (10, 5),
                "expressions": [("a", "5"), ("10", "5")]
            }
    ),
    (  # (a, 5, a + 4)
            ast.Load(),
            [
                ast.Name(id="a", ctx=ast.Load()),
                ast.Constant(value=5),
                ast.BinOp(left=ast.Name(id="a", ctx=ast.Load()), op=ast.Add(), right=ast.Constant(value=4))
            ],
            {
                "value": (10, 5, 14),
                "expressions": [("a", "5", "a + 4"), ("10", "5", "10 + 4"), ("10", "5", "14")]
            }
    ),
])
def test__calculate_node(create_ast_tuple, elem_manager, ctx, elts, expect_result):
    ast_tuple = create_ast_tuple(ctx=ctx, elts=elts)
    tuple_parser = TupleParser(ast_tuple, elem_manager)

    with patch('app.analysis.util.util.transpose_with_last_fill') as mock_transpose:
        mock_transpose.side_effect = (
            lambda expressions:
            [["a", "5"], ["10", "5"]]
            if expressions == [["a", "10"], ["5"]]
            else
            [["a", "5", "a + 4"], ["10", "5", "10 + 4"], ["10", "5", "14"]]
            if expressions == [["a", "10"], ["5"], ["a + 4", "10 + 4", "14"]]
            else []
        )

        result = tuple_parser._TupleParser__calculate_node()

    assert result == expect_result
