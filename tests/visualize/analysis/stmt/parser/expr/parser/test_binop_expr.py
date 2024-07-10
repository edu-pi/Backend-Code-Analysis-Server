import ast

import pytest

from app.visualize.analysis.stmt.parser.expr.models.expr_obj import ExprObj, BinopObj
from app.visualize.analysis.stmt.parser.expr.parser.binop_expr import BinopExpr


@pytest.mark.parametrize(
    "value, expressions",
    [
        pytest.param(11, ("10 + 1", "11"), id="10 + 1: success case"),
        pytest.param("Hello World", ("'Hello' + ' World'", "'Hello World'"), id="'Hello' + 'World': success case"),
        pytest.param(104, ("a + 1", "104"), id="a: success case"),
        pytest.param("****", ("'*' * 4", "'****'"), id="'*' * 4: success case"),
    ],
)
def test_parse(mocker, value, expressions):
    # ExprObj에 들어갈 값 객체
    value = "mocked_value"
    expressions = ("mocked_expression",)

    mock_left_obj = mocker.MagicMock(spec=ExprObj, value=value, expressions=expressions)
    mock_right_obj = mocker.MagicMock(spec=ExprObj, value=value, expressions=expressions)
    mock_op = mocker.MagicMock(spec=ast)

    mocker.patch(
        "app.visualize.analysis.stmt.parser.expr.parser.binop_expr.BinopExpr._calculate_value", return_value=value
    )
    mocker.patch(
        "app.visualize.analysis.stmt.parser.expr.parser.binop_expr.BinopExpr._create_expressions",
        return_value=expressions,
    )

    result = BinopExpr.parse(mock_left_obj, mock_right_obj, mock_op)

    assert isinstance(result, BinopObj)
    assert result.value == value
    assert result.expressions == expressions


@pytest.mark.parametrize(
    "left_value, right_value, op, expected",
    [
        pytest.param(1, 2, ast.Add(), 3, id="1 + 2: success case"),
        pytest.param(3, 1, ast.Sub(), 2, id="3 - 1: success case"),
        pytest.param(3, 2, ast.Mult(), 6, id="3 * 2: success case"),
        pytest.param(3, 2, ast.Div(), 1.5, id="3 / 2: success case"),
        pytest.param(3, 2, ast.FloorDiv(), 1, id="3 // 2: success case"),
    ],
)
def test_calculate_value(left_value, right_value, op, expected):
    result = BinopExpr._calculate_value(left_value, right_value, op)
    assert result == expected


@pytest.mark.parametrize(
    "left_obj, right_obj, op, value, expected",
    [
        pytest.param(("1",), ("2",), ast.Add(), 3, ("1 + 2", "3"), id="1 + 2: success case"),
        pytest.param(("a", "3"), ("1",), ast.Add(), 4, ("a + 1", "3 + 1", "4"), id="a + 1: success case"),
        pytest.param(
            ("a", "3"),
            ("b + 1", "2 + 1", "3"),
            ast.Add(),
            6,
            ("a + b + 1", "3 + 2 + 1", "3 + 3", "6"),
            id="a + b + 1: success case",
        ),
        pytest.param(
            ("a + 1", "3 + 1", "4"),
            ("b + 2", "2 + 2", "4"),
            ast.Add(),
            8,
            ("a + 1 + b + 2", "3 + 1 + 2 + 2", "4 + 4", "8"),
            id="a + 1 + b + 2: success case",
        ),
        pytest.param(
            ("a + 1", "3 + 1", "4"),
            ("b + 2", "2 + 2", "4"),
            ast.Mult(),
            8,
            ("a + 1 * b + 2", "3 + 1 * 2 + 2", "4 * 4", "8"),
            id="a + 1 * b + 2: success case",
        ),
    ],
)
def test_creat_expressions(left_obj, right_obj, op, value, expected):
    result = BinopExpr._create_expressions(left_obj, right_obj, op, value)
    assert result == expected


@pytest.mark.parametrize(
    "left_expression, right_expression, op, expected",
    [
        pytest.param("a", "b", ast.Add(), "a + b", id="a + b: success case"),
        pytest.param("a", "b", ast.Sub(), "a - b", id="a - b: success case"),
        pytest.param("a", "b", ast.Mult(), "a * b", id="a * b: success case"),
        pytest.param("a", "b", ast.Div(), "a / b", id="a / b: success case"),
        pytest.param("a", "b", ast.FloorDiv(), "a // b", id="a // b: success case"),
    ],
)
def test_concat_expression(left_expression, right_expression, op, expected):
    result = BinopExpr._concat_expression(left_expression, right_expression, op)
    assert result == expected
