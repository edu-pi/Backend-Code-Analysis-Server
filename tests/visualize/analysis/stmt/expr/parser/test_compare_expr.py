import ast

import pytest

from app.visualize.analysis.stmt.expr.parser.compare_expr import CompareExpr


@pytest.mark.parametrize(
    "left_value, right_value, op, expected",
    [
        (3, 3, ast.Eq(), True),  # 3 == 3
        (1, 12, ast.NotEq(), True),  # 1 != 12
        (1, 12, ast.Lt(), True),  # 1 < 12
        (12, 12, ast.LtE(), True),  # 12 <= 12
        (9, 12, ast.LtE(), True),  # 9 <= 12
        (20, 10, ast.Gt(), True),  # 20 > 10
        (20, 20, ast.GtE(), True),  # 20 >= 20,
        (30, 20, ast.GtE(), True),  # 30 >= 20
        ("a", ["a", "b", "c"], ast.In(), True),
        ("d", ["a", "b", "c"], ast.NotIn(), True),
    ],
)
def test_calculate_value(left_value, right_value, op, expected):
    result = CompareExpr._calculate_value(left_value, right_value, op)
    assert result == expected


def test_calculate_value_Is():
    list1 = [1, 2, 3]
    list2 = list1

    result = CompareExpr._calculate_value(list1, list2, ast.Is())
    assert result == True


@pytest.mark.parametrize(
    "left_value, right_value, op, expected",
    [
        (3, 4, ast.Eq(), False),  # 3 == 4
        (12, 12, ast.NotEq(), False),  # 12 != 12
        (14, 12, ast.Lt(), False),  # 14 < 12
        (10, 20, ast.Gt(), False),  # 10 > 20
        (19, 20, ast.GtE(), False),  # 19 >= 20,
        ("d", ["a", "b", "c"], ast.In(), False),
        ("a", ["a", "b", "c"], ast.NotIn(), False),
    ],
)
def test_calculate_value_fail(left_value, right_value, op, expected):
    result = CompareExpr._calculate_value(left_value, right_value, op)
    assert result == expected
