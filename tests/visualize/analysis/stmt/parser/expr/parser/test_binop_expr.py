import ast

import pytest

from app.visualize.analysis.stmt.parser.expr.models.expr_obj import ExprObj, BinopObj, ConstantObj, NameObj
from app.visualize.analysis.stmt.parser.expr.models.expr_type import ExprType
from app.visualize.analysis.stmt.parser.expr.parser.binop_expr import BinopExpr


@pytest.mark.parametrize(
    "left_obj, right_obj, op, expected",
    [
        pytest.param(
            ConstantObj(value=10, expressions=("10",)),
            ConstantObj(value=1, expressions=("1",)),
            ast.Add(),
            BinopObj(value=11, expressions=("10 + 1", "11")),
            id="10 + 1: success case",
        ),
        pytest.param(
            ConstantObj(value="Hello", expressions=("Hello",)),
            ConstantObj(value="World", expressions=("World",)),
            ast.Add(),
            BinopObj(value="HelloWorld", expressions=("Hello + World", "HelloWorld")),
            id="'Hello' + 'World': success case",
        ),
        pytest.param(
            NameObj(value=10, expressions=("a", "10"), type=ExprType.VARIABLE),
            ConstantObj(value=1, expressions=("1",)),
            ast.Add(),
            BinopObj(value=11, expressions=("a + 1", "10 + 1", "11")),
            id="a + 1: success case",
        ),
        pytest.param(
            ConstantObj(value="*", expressions=("'*'",)),
            ConstantObj(value=4, expressions=("4",)),
            ast.Mult(),
            BinopObj(value="****", expressions=("* * 4", "****")),
            id="'*' * 4: success case",
        ),
    ],
)
def test_parse(mocker, left_obj: ExprObj, right_obj: ExprObj, op: ast, expected: BinopObj):
    mock_calculate_value = mocker.patch.object(BinopExpr, "_calculate_value", return_value=expected.value)
    mock_create_expressions = mocker.patch.object(BinopExpr, "_create_expressions", return_value=expected.expressions)

    result = BinopExpr.parse(left_obj, right_obj, op)

    assert result == expected
    mock_calculate_value.assert_called_once_with(left_obj.value, right_obj.value, op)
    mock_create_expressions.assert_called_once_with(left_obj.expressions, right_obj.expressions, op, expected.value)


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
