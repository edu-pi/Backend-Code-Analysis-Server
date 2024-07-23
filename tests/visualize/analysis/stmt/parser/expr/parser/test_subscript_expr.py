import pytest

from app.visualize.analysis.stmt.parser.expr.models.expr_obj import (
    NameObj,
    ConstantObj,
    SliceObj,
    ExprObj,
    SubscriptObj,
)
from app.visualize.analysis.stmt.parser.expr.models.expr_type import ExprType
from app.visualize.analysis.stmt.parser.expr.models.slice_expression import SliceExpression
from app.visualize.analysis.stmt.parser.expr.parser.subscript_expr import SubscriptExpr


@pytest.mark.parametrize(
    "target_obj, slice_obj, expected",
    [
        pytest.param(
            NameObj(
                value=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
                expressions=("a", "[0, 1, 2, 3, 4, 5, 6, 7, 8, 9]"),
                type=ExprType.LIST,
            ),
            ConstantObj(value=0, expressions=("0",)),
            SubscriptObj(value=0, expressions=("a[0]", "0")),
            id="a[0] success case",
        ),
        pytest.param(
            NameObj(
                value=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
                expressions=("a", "[0, 1, 2, 3, 4, 5, 6, 7, 8, 9]"),
                type=ExprType.LIST,
            ),
            SliceObj(value=slice(2, 5), expressions=(SliceExpression(lower="2", upper="5"),)),
            SubscriptObj(value=[2, 3, 4], expressions=("a[2:5]", "[2, 3, 4]")),
            id="a[2:5] success case",
        ),
        pytest.param(
            NameObj(
                value=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
                expressions=("a", "[0, 1, 2, 3, 4, 5, 6, 7, 8, 9]"),
                type=ExprType.LIST,
            ),
            SliceObj(
                value=slice(2, 5),
                expressions=(SliceExpression(lower="2", upper="a"), SliceExpression(lower="2", upper="5")),
            ),
            SubscriptObj(value=[2, 3, 4], expressions=("a[2:a]", "a[2:5]", "[2, 3, 4]")),
            id="a[2:a] success case",
        ),
        pytest.param(
            NameObj(
                value=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
                expressions=("a", "[0, 1, 2, 3, 4, 5, 6, 7, 8, 9]"),
                type=ExprType.LIST,
            ),
            SliceObj(value=slice(2, 10, 2), expressions=(SliceExpression(lower="2", upper="10", step="2"),)),
            SubscriptObj(value=[2, 4, 6, 8], expressions=("a[2:10:2]", "[2, 4, 6, 8]")),
            id="a[2:10:2] success case",
        ),
        pytest.param(
            NameObj(
                value=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
                expressions=("a", "[0, 1, 2, 3, 4, 5, 6, 7, 8, 9]"),
                type=ExprType.LIST,
            ),
            SliceObj(value=slice(0, 5), expressions=(SliceExpression(lower="0", upper="5"),)),
            SubscriptObj(value=[0, 1, 2, 3, 4], expressions=("a[0:5]", "[0, 1, 2, 3, 4]")),
            id="a[:5] success case",
        ),
        pytest.param(
            NameObj(
                value=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
                expressions=("a", "[0, 1, 2, 3, 4, 5, 6, 7, 8, 9]"),
                type=ExprType.LIST,
            ),
            SliceObj(value=slice(3, 10), expressions=(SliceExpression(lower="3", upper="10"),)),
            SubscriptObj(value=[3, 4, 5, 6, 7, 8, 9], expressions=("a[3:10]", "[3, 4, 5, 6, 7, 8, 9]")),
            id="a[3:] success case",
        ),
        pytest.param(
            NameObj(
                value=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
                expressions=("a", "[0, 1, 2, 3, 4, 5, 6, 7, 8, 9]"),
                type=ExprType.LIST,
            ),
            SliceObj(value=slice(0, 10), expressions=(SliceExpression(lower="0", upper="10"),)),
            SubscriptObj(
                value=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9], expressions=("a[0:10]", "[0, 1, 2, 3, 4, 5, 6, 7, 8, 9]")
            ),
            id="a[:] success case",
        ),
    ],
)
def test_parse(mocker, target_obj: ExprObj, slice_obj: ExprObj, expected: SubscriptObj):
    mock_get_value = mocker.patch.object(SubscriptExpr, "_get_value", return_value=expected.value)
    mock_create_expressions = mocker.patch.object(
        SubscriptExpr, "_create_expressions", return_value=expected.expressions
    )

    result = SubscriptExpr.parse(target_obj, slice_obj)

    assert isinstance(result, SubscriptObj)
    mock_get_value.assert_called_once_with(target_obj.value, slice_obj.value)
    mock_create_expressions.assert_called_once_with(target_obj, slice_obj)


@pytest.mark.parametrize(
    "slice_obj_value, expected",
    [
        pytest.param(0, 0, id="a[0] success case"),
        pytest.param(slice(2, 5), [2, 3, 4], id="a[2:5] success case"),
        pytest.param(slice(2, 10, 2), [2, 4, 6, 8], id="a[2:10:2] success case"),
        pytest.param(slice(0, 5), [0, 1, 2, 3, 4], id="a[:5] success case"),
        pytest.param(slice(3, 10), [3, 4, 5, 6, 7, 8, 9], id="a[3:] success case"),
        pytest.param(slice(0, 10), [0, 1, 2, 3, 4, 5, 6, 7, 8, 9], id="a[:] success case"),
    ],
)
def test_get_value(slice_obj_value: int, expected):
    target_obj_value = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    result = SubscriptExpr._get_value(target_obj_value, slice_obj_value)

    assert result == expected


@pytest.mark.parametrize(
    "target_obj, slice_obj, expected",
    [
        pytest.param(
            NameObj(
                value=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
                expressions=("a", "[0, 1, 2, 3, 4, 5, 6, 7, 8, 9]"),
                type=ExprType.LIST,
            ),
            ConstantObj(value=0, expressions=("0",)),
            ("a[0]", "0"),
            id="a[0] success case",
        ),
        pytest.param(
            NameObj(
                value=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
                expressions=("a", "[0, 1, 2, 3, 4, 5, 6, 7, 8, 9]"),
                type=ExprType.LIST,
            ),
            NameObj(value=0, expressions=("idx", "0"), type=ExprType.VARIABLE),
            ("a[idx]", "a[0]", "0"),
            id="a[idx] success case",
        ),
    ],
)
def test_create_expressions_with_single_slice(target_obj: ExprObj, slice_obj: ExprObj, expected):
    result = SubscriptExpr._create_expressions(target_obj, slice_obj)

    assert result == expected


@pytest.mark.parametrize(
    "target_obj, slice_obj, expected",
    [
        pytest.param(
            NameObj(
                value=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
                expressions=("a", "[0, 1, 2, 3, 4, 5, 6, 7, 8, 9]"),
                type=ExprType.LIST,
            ),
            SliceObj(value=slice(2, 5), expressions=(SliceExpression(lower="2", upper="5"),)),
            ("a[2:5]", "[2, 3, 4]"),
            id="a[2:5] success case",
        ),
        pytest.param(
            NameObj(
                value=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
                expressions=("a", "[0, 1, 2, 3, 4, 5, 6, 7, 8, 9]"),
                type=ExprType.LIST,
            ),
            SliceObj(
                value=slice(2, 5),
                expressions=(SliceExpression(lower="2", upper="a"), SliceExpression(lower="2", upper="5")),
            ),
            ("a[2:a]", "a[2:5]", "[2, 3, 4]"),
            id="a[2:a] success case",
        ),
        pytest.param(
            NameObj(
                value=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
                expressions=("a", "[0, 1, 2, 3, 4, 5, 6, 7, 8, 9]"),
                type=ExprType.LIST,
            ),
            SliceObj(value=slice(2, 10, 2), expressions=(SliceExpression(lower="2", upper="10", step="2"),)),
            ("a[2:10:2]", "[2, 4, 6, 8]"),
            id="a[2:10:2] success case",
        ),
        pytest.param(
            NameObj(
                value=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
                expressions=("a", "[0, 1, 2, 3, 4, 5, 6, 7, 8, 9]"),
                type=ExprType.LIST,
            ),
            SliceObj(value=slice(0, 5), expressions=(SliceExpression(upper="5"),)),
            ("a[:5]", "[0, 1, 2, 3, 4]"),
            id="a[:5] success case",
        ),
        pytest.param(
            NameObj(
                value=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
                expressions=("a", "[0, 1, 2, 3, 4, 5, 6, 7, 8, 9]"),
                type=ExprType.LIST,
            ),
            SliceObj(value=slice(3, 10), expressions=(SliceExpression(lower="3"),)),
            ("a[3:]", "[3, 4, 5, 6, 7, 8, 9]"),
            id="a[3:] success case",
        ),
        pytest.param(
            NameObj(
                value=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
                expressions=("a", "[0, 1, 2, 3, 4, 5, 6, 7, 8, 9]"),
                type=ExprType.LIST,
            ),
            SliceObj(value=slice(0, 10), expressions=(SliceExpression(),)),
            ("a[:]", "[0, 1, 2, 3, 4, 5, 6, 7, 8, 9]"),
            id="a[:] success case",
        ),
    ],
)
def test_create_expressions_with_multiple_slice(target_obj: ExprObj, slice_obj: ExprObj, expected):
    result = SubscriptExpr._create_expressions(target_obj, slice_obj)

    assert result == expected
