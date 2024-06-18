import ast
from unittest.mock import MagicMock, patch

import pytest

from app.analysis.element_manager import CodeElementManager
from app.analysis.generator.parser.binop_parser import BinopParser, Binop


@pytest.fixture
def elem_manager():
    mock = MagicMock(spec=CodeElementManager)
    mock.get_variable_value.return_value = 10
    return mock


@pytest.fixture
def create_binop():
    def _create_binop(left, right, op):
        return ast.BinOp(left=left, right=right, op=op)

    return _create_binop


@pytest.fixture
def create_binop_parser(elem_manager):
    mock_binop_parser = MagicMock(spec=BinopParser)
    mock_binop_parser.side_effect = lambda node: BinopParser(node, elem_manager)
    return mock_binop_parser


def create_param():
    return [
        (  # a + 4
            ast.Name(id="a", ctx=ast.Load()),
            ast.Constant(value=4),
            ast.Add(),
            14,
            ["a + 4", "10 + 4" "14"]
        ),
        (  # (a - 5) - 4
            ast.BinOp(left=ast.Name(id="a", ctx=ast.Load()), op=ast.Sub(), right=ast.Constant(value=5)),
            ast.Constant(value=4),
            ast.Sub(),
            1,
            ["(a - 5) - 4", "(10 - 5) - 4", "1"]),
        (  # 4 * b
            ast.Constant(value=4),
            ast.Name(id="b", ctx=ast.Load()),
            ast.Mult(),
            40,
            ["4 * b", "4 * 10" "40"]),
        (  # 40 / b
            ast.Constant(value=40),
            ast.Name(id="b", ctx=ast.Load()),
            ast.Div(),
            4.0,
            ["40 / b", "40 / 10" "4.0"]),
        (  # a // b
            ast.Name(id="a", ctx=ast.Load()),
            ast.Name(id="b", ctx=ast.Load()),
            ast.FloorDiv(),
            1,
            ["a // b", "10 // 10" "1"])
    ]


@pytest.mark.parametrize("left, right, op, expect_value, expect_expressions", create_param())
def test_parse(create_binop, elem_manager, left, right, op, expect_value, expect_expressions):
    binop = create_binop(left=left, op=op, right=right)

    with patch.object(BinopParser, '_BinopParser__calculate_node', return_value=expect_value), \
            patch.object(BinopParser, '_BinopParser__create_expressions', return_value=expect_expressions):
        result = BinopParser.parse(binop, elem_manager)

        assert result == Binop(value=expect_value, expressions=expect_expressions)
        assert result.value == expect_value
        assert result.expressions == expect_expressions


@pytest.mark.parametrize("left, right, op, expect_value, expect_expressions", create_param())
def test__calculate_node(create_binop, create_binop_parser, left, right, op, expect_value, expect_expressions):
    binop = create_binop(left=left, op=op, right=right)
    binop_parser = create_binop_parser(binop)

    with patch.object(BinopParser, '_BinopParser__calculate_value', return_value=expect_value):
        result = binop_parser._BinopParser__calculate_node(binop)

        assert result == expect_value


@pytest.mark.parametrize("left_value, right_value, op, expect", [
    (1, 2, ast.Add(), 3),
    (3, 2, ast.Sub(), 1),
    (2, 4, ast.Mult(), 8),
    (4, 2, ast.Div(), 2.0),
    (4, 2, ast.FloorDiv(), 2)
])
def test__calculate_value(create_binop_parser, create_binop, left_value, right_value, op, expect):
    binop = create_binop(left=ast.Constant(value=left_value), op=op, right=ast.Constant(value=right_value))
    binop_parser = create_binop_parser(binop)

    result = binop_parser._BinopParser__calculate_value(left_value=left_value, right_value=right_value, op=op)

    assert result == expect


@pytest.mark.parametrize("left_value, right_value, op, result_value, expect", [
    (1, 2, ast.Add(), 3, ["1 + 2", "3"]),
    (2, 1, ast.Sub(), 1, ["2 - 1", "1"]),
    (2, 2, ast.Mult(), 4, ["2 * 2", "4"]),
    (4, 2, ast.Div(), 2.0, ["4 / 2", "2.0"]),
    (4, 2, ast.FloorDiv(), 2, ["4 // 2", "2"])
])
def test__create_expressions(create_binop_parser, create_binop, left_value, right_value, op, result_value, expect):
    binop = create_binop(left=ast.Constant(value=left_value), op=op, right=ast.Constant(value=right_value))
    binop_parser = create_binop_parser(binop)

    result = binop_parser._BinopParser__create_expressions(result_value=result_value,
                                                           initial_expression=ast.unparse(binop))

    assert result == expect
