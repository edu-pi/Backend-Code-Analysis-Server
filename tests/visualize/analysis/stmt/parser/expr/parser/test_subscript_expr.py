import ast

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
    "target_obj, slice_obj, ctx, expected",
    [
        pytest.param(
            NameObj(
                value=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
                expressions=("a", "[0, 1, 2, 3, 4, 5, 6, 7, 8, 9]"),
                type=ExprType.LIST,
            ),
            ConstantObj(value=0, expressions=("0",)),
            ast.Load(),
            SubscriptObj(value=0, expressions=("a[0]", "0"), type=ExprType.LIST),
            id="a[0] - ast.Load: success case",
        ),
        pytest.param(
            NameObj(
                value=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
                expressions=("a", "[0, 1, 2, 3, 4, 5, 6, 7, 8, 9]"),
                type=ExprType.LIST,
            ),
            SliceObj(value=slice(2, 5), expressions=(SliceExpression(lower="2", upper="5"),)),
            ast.Load(),
            SubscriptObj(value=[2, 3, 4], expressions=("a[2:5]", "[2, 3, 4]"), type=ExprType.LIST),
            id="a[2:5] - ast.Load: success case",
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
            ast.Load(),
            SubscriptObj(value=[2, 3, 4], expressions=("a[2:a]", "a[2:5]", "[2, 3, 4]"), type=ExprType.LIST),
            id="a[2:a] - ast.Load: success case",
        ),
        pytest.param(
            NameObj(
                value=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
                expressions=("a", "[0, 1, 2, 3, 4, 5, 6, 7, 8, 9]"),
                type=ExprType.LIST,
            ),
            SliceObj(value=slice(2, 10, 2), expressions=(SliceExpression(lower="2", upper="10", step="2"),)),
            ast.Load(),
            SubscriptObj(value=[2, 4, 6, 8], expressions=("a[2:10:2]", "[2, 4, 6, 8]"), type=ExprType.LIST),
            id="a[2:10:2] - ast.Load: success case",
        ),
        pytest.param(
            NameObj(
                value=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
                expressions=("a", "[0, 1, 2, 3, 4, 5, 6, 7, 8, 9]"),
                type=ExprType.LIST,
            ),
            SliceObj(value=slice(0, 5), expressions=(SliceExpression(lower="0", upper="5"),)),
            ast.Load(),
            SubscriptObj(value=[0, 1, 2, 3, 4], expressions=("a[0:5]", "[0, 1, 2, 3, 4]"), type=ExprType.LIST),
            id="a[:5] - ast.Load: success case",
        ),
        pytest.param(
            NameObj(
                value=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
                expressions=("a", "[0, 1, 2, 3, 4, 5, 6, 7, 8, 9]"),
                type=ExprType.LIST,
            ),
            SliceObj(value=slice(3, 10), expressions=(SliceExpression(lower="3", upper="10"),)),
            ast.Load(),
            SubscriptObj(
                value=[3, 4, 5, 6, 7, 8, 9], expressions=("a[3:10]", "[3, 4, 5, 6, 7, 8, 9]"), type=ExprType.LIST
            ),
            id="a[3:] - ast.Load: success case",
        ),
        pytest.param(
            NameObj(
                value=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
                expressions=("a", "[0, 1, 2, 3, 4, 5, 6, 7, 8, 9]"),
                type=ExprType.LIST,
            ),
            SliceObj(value=slice(0, 10), expressions=(SliceExpression(lower="0", upper="10"),)),
            ast.Load(),
            SubscriptObj(
                value=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
                expressions=("a[0:10]", "[0, 1, 2, 3, 4, 5, 6, 7, 8, 9]"),
                type=ExprType.LIST,
            ),
            id="a[:] - ast.Load: success case",
        ),
        pytest.param(
            NameObj(
                value=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
                expressions=("a", "[0, 1, 2, 3, 4, 5, 6, 7, 8, 9]"),
                type=ExprType.LIST,
            ),
            ConstantObj(value=0, expressions=("0",)),
            ast.Store(),
            SubscriptObj(value="a[0]", expressions=("a[0]", "0"), type=ExprType.LIST),
            id="a[0] - ast.Store: success case",
        ),
        pytest.param(
            NameObj(
                value=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
                expressions=("a", "[0, 1, 2, 3, 4, 5, 6, 7, 8, 9]"),
                type=ExprType.LIST,
            ),
            SliceObj(value=slice(2, 5), expressions=(SliceExpression(lower="2", upper="5"),)),
            ast.Store(),
            SubscriptObj(value="a[2:5]", expressions=("a[2:5]", "[2, 3, 4]"), type=ExprType.LIST),
            id="a[2:5] - ast.Store: success case",
        ),
    ],
)
def test_parse(mocker, target_obj: ExprObj, slice_obj: ExprObj, ctx, expected: SubscriptObj):
    mock_get_value = mocker.patch.object(SubscriptExpr, "_get_value", return_value=expected.value)
    mock_create_expressions = mocker.patch.object(
        SubscriptExpr, "_create_expressions", return_value=expected.expressions
    )
    mock_expr_type = mocker.patch.object(ExprType, "judge_collection_type", return_value=expected.type)

    result = SubscriptExpr.parse(target_obj, slice_obj, ctx)

    assert isinstance(result, SubscriptObj)
    mock_get_value.assert_called_once_with(target_obj, slice_obj, ctx)
    mock_expr_type.assert_called_once_with(expected.value)


@pytest.mark.parametrize(
    "slice_obj_value, expected",
    [
        pytest.param(
            ConstantObj(value=0, expressions=("0",)),
            0,
            id="a[0] success case",
        ),
        pytest.param(
            SliceObj(value=slice(2, 5), expressions=(SliceExpression(upper="2", lower="5"),)),
            [2, 3, 4],
            id="a[2:5] success case",
        ),
        pytest.param(
            SliceObj(value=slice(2, 10, 2), expressions=(SliceExpression(upper="2", lower="10", step="2"),)),
            [2, 4, 6, 8],
            id="a[2:10:2] success case",
        ),
        pytest.param(
            SliceObj(value=slice(0, 5), expressions=(SliceExpression(upper="0", lower="5"),)),
            [0, 1, 2, 3, 4],
            id="a[:5] success case",
        ),
    ],
)
def test_get_value_load(slice_obj_value: ExprObj, expected):
    target_obj_value = NameObj(
        value=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
        expressions=("l", "[0, 1, 2, 3, 4, 5, 6, 7, 8, 9]"),
        type=ExprType.LIST,
    )
    result = SubscriptExpr._get_value(target_obj_value, slice_obj_value, ast.Load())

    assert result == expected


@pytest.mark.parametrize(
    "target_obj_value, slice_obj_value, expected",
    [
        pytest.param(
            NameObj(
                value=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
                expressions=("l", "[0, 1, 2, 3, 4, 5, 6, 7, 8, 9]"),
                type=ExprType.LIST,
            ),
            ConstantObj(value=0, expressions=("0",)),
            "l[0]",
            id="a[0] success case",
        ),
        pytest.param(
            NameObj(
                value=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
                expressions=("l", "[0, 1, 2, 3, 4, 5, 6, 7, 8, 9]"),
                type=ExprType.LIST,
            ),
            SliceObj(value=slice(0, 5), expressions=(SliceExpression(lower="0", upper="5"),)),
            "l[0:5]",
            id="a[:5] success case",
        ),
        pytest.param(
            NameObj(
                value={"key1": "value1", "key2": "value2"},
                expressions=("d", "{'key1': 'value1', 'key2': 'value2'}"),
                type=ExprType.LIST,
            ),
            ConstantObj(value="key1", expressions=("key1",)),
            "d[key1]",
            id="d['key1'] success case",
        ),
    ],
)
def test_get_value_store(target_obj_value: ExprObj, slice_obj_value: ExprObj, expected):
    result = SubscriptExpr._get_value(target_obj_value, slice_obj_value, ast.Store())

    assert result == expected


@pytest.mark.parametrize(
    "target_obj, slice_obj, subscript_value, expected",
    [
        pytest.param(
            NameObj(
                value=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
                expressions=("a", "[0, 1, 2, 3, 4, 5, 6, 7, 8, 9]"),
                type=ExprType.LIST,
            ),
            ConstantObj(value=0, expressions=("0",)),
            0,
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
            0,
            ("a[idx]", "a[0]", "0"),
            id="a[idx] success case",
        ),
    ],
)
def test_create_expressions_with_single_slice(target_obj: ExprObj, slice_obj: ExprObj, subscript_value, expected):
    result = SubscriptExpr._create_expressions(target_obj, slice_obj, subscript_value)

    assert result == expected


@pytest.mark.parametrize(
    "target_obj, slice_obj, subscript_value, expected",
    [
        pytest.param(
            NameObj(
                value=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
                expressions=("a", "[0, 1, 2, 3, 4, 5, 6, 7, 8, 9]"),
                type=ExprType.LIST,
            ),
            SliceObj(value=slice(2, 5), expressions=(SliceExpression(lower="2", upper="5"),)),
            [2, 3, 4],
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
            [2, 3, 4],
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
            [2, 4, 6, 8],
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
            [0, 1, 2, 3, 4],
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
            [3, 4, 5, 6, 7, 8, 9],
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
            [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
            ("a[:]", "[0, 1, 2, 3, 4, 5, 6, 7, 8, 9]"),
            id="a[:] success case",
        ),
    ],
)
def test_create_expressions_with_multiple_slice(target_obj: ExprObj, slice_obj: ExprObj, subscript_value, expected):
    result = SubscriptExpr._create_expressions(target_obj, slice_obj, subscript_value)

    assert result == expected
