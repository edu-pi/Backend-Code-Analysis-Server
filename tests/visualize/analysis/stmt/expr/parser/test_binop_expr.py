import ast

import pytest

from app.visualize.analysis.stmt.expr.model.expr_obj import ExprObj, NameObj, BinopObj, ConstantObj
from app.visualize.analysis.stmt.expr.parser.binop_expr import BinopExpr


@pytest.mark.parametrize(
    "left_obj, right_obj, op, expected",
    [
        (
            NameObj(value=1, expressions=("a", "1")),
            NameObj(value=2, expressions=("b", "2")),
            ast.Add(),
            BinopObj(value=3, expressions=("a + b", "1 + 2", "3")),
        ),
        (
            NameObj(value=2, expressions=("a", "2")),
            ConstantObj(value=2, expressions=tuple("2")),
            ast.Sub(),
            BinopObj(value=0, expressions=("a - 2", "2 - 2", "0")),
        ),
        (
            BinopObj(value=3, expressions=("a + 1", "2 + 1", "3")),
            BinopObj(value=2, expressions=("b + 1", "1 + 1", "2")),
            ast.Mult(),
            BinopObj(value=6, expressions=("a + 1 * b + 1", "2 + 1 * 1 + 1", "3 * 2", "6")),
        ),
        (
            BinopObj(value=3, expressions=("a + 1", "2 + 1", "3")),
            ConstantObj(value=2, expressions=tuple("2")),
            ast.Div(),
            BinopObj(value=1.5, expressions=("a + 1 / 2", "2 + 1 / 2", "3 / 2", "1.5")),
        ),
        (
            BinopObj(value=3, expressions=("a + 1", "2 + 1", "3")),
            ConstantObj(value=2, expressions=tuple("2")),
            ast.FloorDiv(),
            BinopObj(value=1, expressions=("a + 1 // 2", "2 + 1 // 2", "3 // 2", "1")),
        ),
    ],
)
def test_parse(left_obj, right_obj, op, expected):
    result = BinopExpr.parse(left_obj, right_obj, op)
    assert result == expected


@pytest.mark.parametrize(
    "left_value, right_value, op, expected",
    [
        (1, 2, ast.Add(), 3),
        (3, 1, ast.Sub(), 2),
        (3, 2, ast.Mult(), 6),
        (3, 2, ast.Div(), 1.5),
        (3, 2, ast.FloorDiv(), 1),
    ],
)
def test_calculate_value(left_value, right_value, op, expected):
    result = BinopExpr._calculate_value(left_value, right_value, op)
    assert result == expected


@pytest.mark.parametrize(
    "left_obj, right_obj, op, value, expected",
    [
        (("1"), ("2"), ast.Add(), 3, ("1 + 2", "3")),
        (("a", "3"), ("1"), ast.Add(), 4, ("a + 1", "3 + 1", "4")),
        (("a", "3"), ("b + 1", "2 + 1", "3"), ast.Add(), 6, ("a + b + 1", "3 + 2 + 1", "3 + 3", "6")),
        (
            ("a + 1", "3 + 1", "4"),
            ("b + 2", "2 + 2", "4"),
            ast.Add(),
            8,
            ("a + 1 + b + 2", "3 + 1 + 2 + 2", "4 + 4", "8"),
        ),
        (
            ("a + 1", "3 + 1", "4"),
            ("b + 2", "2 + 2", "4"),
            ast.Mult(),
            8,
            ("a + 1 * b + 2", "3 + 1 * 2 + 2", "4 * 4", "8"),
        ),
    ],
)
def test_creat_expressions(left_obj, right_obj, op, value, expected):
    result = BinopExpr._create_expressions(left_obj, right_obj, op, value)
    assert result == expected


@pytest.mark.parametrize(
    "left_expression, right_expression, op, expected",
    [
        ("a", "b", ast.Add(), "a + b"),
        ("a", "b", ast.Sub(), "a - b"),
        ("a", "b", ast.Mult(), "a * b"),
        ("a", "b", ast.Div(), "a / b"),
        ("a", "b", ast.FloorDiv(), "a // b"),
    ],
)
def test_concat_expression(left_expression, right_expression, op, expected):
    result = BinopExpr._concat_expression(left_expression, right_expression, op)
    assert result == expected
