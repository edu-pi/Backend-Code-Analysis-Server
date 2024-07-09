import ast

import pytest

from app.visualize.analysis.stmt.parser.expr.models.expr_obj import ExprObj, NameObj, BinopObj, ConstantObj
from app.visualize.analysis.stmt.parser.expr.parser.binop_expr import BinopExpr


@pytest.mark.parametrize(
    "left_obj, right_obj, op, expected",
    [
        pytest.param(
            NameObj(value=1, expressions=("a", "1")),
            NameObj(value=2, expressions=("b", "2")),
            ast.Add(),
            BinopObj(value=3, expressions=("a + b", "1 + 2", "3")),
            id="a + b: success case",
        ),
        pytest.param(
            NameObj(value=2, expressions=("a", "2")),
            ConstantObj(value=2, expressions=tuple("2")),
            ast.Sub(),
            BinopObj(value=0, expressions=("a - 2", "2 - 2", "0")),
            id="a - 2: success case",
        ),
        pytest.param(
            BinopObj(value=3, expressions=("a + 1", "2 + 1", "3")),
            BinopObj(value=2, expressions=("b + 1", "1 + 1", "2")),
            ast.Mult(),
            BinopObj(value=6, expressions=("a + 1 * b + 1", "2 + 1 * 1 + 1", "3 * 2", "6")),
            id="a + 1 * b + 1: success case",
        ),
        pytest.param(
            BinopObj(value=3, expressions=("a + 1", "2 + 1", "3")),
            ConstantObj(value=2, expressions=tuple("2")),
            ast.Div(),
            BinopObj(value=1.5, expressions=("a + 1 / 2", "2 + 1 / 2", "3 / 2", "1.5")),
            id="a + 1 / 2: success case",
        ),
        pytest.param(
            BinopObj(value=3, expressions=("a + 1", "2 + 1", "3")),
            ConstantObj(value=2, expressions=tuple("2")),
            ast.FloorDiv(),
            BinopObj(value=1, expressions=("a + 1 // 2", "2 + 1 // 2", "3 // 2", "1")),
            id="a + 1 // 2: success case",
        ),
        pytest.param(
            ConstantObj(value="*", expressions=("'*'",)),
            ConstantObj(value=3, expressions=("3",)),
            ast.Mult(),
            BinopObj(value="***", expressions=("'*' * 3", "'***'")),
            id="'*' * 3: success case",
        ),
    ],
)
def test_parse(left_obj: ExprObj, right_obj: ExprObj, op, expected):
    result = BinopExpr.parse(left_obj, right_obj, op)
    assert result == expected


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
