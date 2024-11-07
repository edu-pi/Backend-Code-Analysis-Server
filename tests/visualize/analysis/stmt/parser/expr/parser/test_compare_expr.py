import ast

import pytest

from app.visualize.analysis.stmt.parser.expr.models.expr_obj import CompareObj, ConstantObj, NameObj, ExprObj
from app.visualize.analysis.stmt.parser.expr.models.expr_type import ExprType
from app.visualize.analysis.stmt.parser.expr.parser.compare_expr import CompareExpr


@pytest.mark.parametrize(
    "left_obj, comparators, ops, expected",
    [
        pytest.param(
            ConstantObj(
                value=1,
                expressions=("1",),
            ),
            (ConstantObj(value=2, expressions=("2",)),),
            (ast.Eq(),),
            CompareObj(value=False, expressions=("1 == 2", "False")),
            id="1==2",
        ),
        pytest.param(
            NameObj(
                value=10,
                expressions=("a", "10"),
                type=ExprType.VARIABLE,
            ),
            (ConstantObj(value=10, expressions=("10",)),),
            (ast.Eq(),),
            CompareObj(value=True, expressions=("a == 10", "10 == 10", "True")),
            id="a==10",
        ),
        pytest.param(
            ConstantObj(
                value=1,
                expressions=("1",),
            ),
            (
                NameObj(value=10, expressions=("a", "10"), type=ExprType.VARIABLE),
                ConstantObj(value=30, expressions=("30",)),
            ),
            (ast.Lt(), ast.Lt()),
            CompareObj(value=True, expressions=("1 < a < 30", "True")),
            id="1 < a < 30",
        ),
    ],
)
def test_parse(left_obj: ExprObj, comparators, ops, expected: CompareObj):
    result = CompareExpr.parse(left_obj, comparators, ops)
    assert result.value == expected.value
    assert result.expressions == expected.expressions


@pytest.mark.parametrize(
    "left_value, right_value, op, expected",
    [
        pytest.param(3, 3, ast.Eq(), True, id="3 == 3"),  # 3 == 3
        pytest.param(1, 12, ast.NotEq(), True, id="1 != 12"),  # 1 != 12
        pytest.param(1, 12, ast.Lt(), True, id="1 < 12"),  # 1 < 12
        pytest.param(12, 12, ast.LtE(), True, id="12 <= 12"),  # 12 <= 12
        pytest.param(9, 12, ast.LtE(), True, id="9 <= 12"),  # 9 <= 12
        pytest.param(20, 10, ast.Gt(), True, id="20 > 10"),  # 20 > 10
        pytest.param(20, 20, ast.GtE(), True, id="20 >= 20,"),  # 20 >= 20,
        pytest.param(30, 20, ast.GtE(), True, id=" 30 >= 20"),  # 30 >= 20
        pytest.param("a", ["a", "b", "c"], ast.In(), True, id="a in ['a', 'b', 'c']"),
        pytest.param("d", ["a", "b", "c"], ast.NotIn(), True, id="d not in ['a', 'b', 'c']"),
    ],
)
def test_calculate_value(left_value, right_value, op: ast.cmpop, expected):
    result = CompareExpr._calculate_value(left_value, right_value, op)
    assert result == expected


def test_calculate_value_Is():
    list1 = [1, 2, 3]
    list2 = list1
    ast_is: ast.Is = ast.Is()

    result = CompareExpr._calculate_value(list1, list2, ast_is)
    assert result is True


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
def test_calculate_value_fail(left_value, right_value, op: ast, expected):
    result = CompareExpr._calculate_value(left_value, right_value, op)
    assert result == expected
