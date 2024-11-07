from unittest.mock import MagicMock

import pytest

from app.visualize.analysis.stmt.parser.expr.models.expr_obj import (
    AttributeObj,
    ExprObj,
    ConstantObj,
    InsertObj,
)
from app.visualize.analysis.stmt.parser.expr.models.expr_type import ExprType
from app.visualize.analysis.stmt.parser.expr.parser.attr_func.insert_expr import InsertExpr


@pytest.mark.parametrize(
    "elem_container_dict, expressions, args, expected",
    [
        pytest.param(
            {"a": [1, 2, 3, 4, 5]},
            ("a", "[1, 2, 3, 4, 5]"),
            [ConstantObj(value=2, expressions=("2",)), ConstantObj(value=1, expressions=("1",))],
            InsertObj(value="a", expressions=("0",)),
            id="a.insert(2, 1): success case",
        ),
    ],
)
def test_parse(mocker, elem_container_dict: dict, expressions: tuple, args: list[ExprObj], expected: AttributeObj):
    mock_insert_value = mocker.patch.object(InsertExpr, "_insert_value", return_value=expected.value)
    mock_get_value = mocker.patch.object(InsertExpr, "_get_value", return_value=expected.value)
    mock_create_expressions = mocker.patch.object(InsertExpr, "_create_expressions", return_value=expected.expressions)

    attr_obj = AttributeObj(
        value=getattr(elem_container_dict["a"], "insert"),
        expressions=expressions,
        type=ExprType.INSERT,
    )

    result = InsertExpr.parse(attr_obj, args)

    assert isinstance(result, InsertObj)
    mock_insert_value.assert_called_once_with(attr_obj, args)
    mock_get_value.assert_called_once_with(attr_obj)
    mock_create_expressions.assert_called_once_with(args)


def test_parse_wrong_arguments():
    attr_obj = MagicMock(spec=AttributeObj)
    args = [MagicMock(spec=ExprObj)]

    with pytest.raises(ValueError):
        InsertExpr.parse(attr_obj, args)


@pytest.mark.parametrize(
    "elem_container_dict, expressions, args",
    [
        pytest.param(
            {"a": [1, 2, 3, 4, 5]},
            ("a", "[1, 2, 3, 4, 5]"),
            [ConstantObj(value=2, expressions=("2",)), ConstantObj(value=1, expressions=("1",))],
            id="a.insert(2, 1): success case",
        ),
    ],
)
def test_insert_value(elem_container_dict: dict, expressions: tuple, args: list[ExprObj]):
    attr_obj = AttributeObj(
        value=getattr(elem_container_dict["a"], "insert"),
        expressions=expressions,
        type=ExprType.INSERT,
    )
    InsertExpr._insert_value(attr_obj, args)

    assert elem_container_dict["a"] == [1, 2, 1, 3, 4, 5]


@pytest.mark.parametrize(
    "elem_container_dict, expressions, expected",
    [
        pytest.param(
            {"a": [1, 2, 3, 4, 5]},
            ("a", "[1, 2, 3, 4, 5]"),
            "a",
            id="a.insert(0): success case",
        )
    ],
)
def test_get_value(elem_container_dict: dict, expressions: tuple, expected: str):
    attr_obj = AttributeObj(
        value=getattr(elem_container_dict["a"], "insert"),
        expressions=expressions,
        type=ExprType.INSERT,
    )
    result = InsertExpr._get_value(attr_obj)

    assert result == expected


@pytest.mark.parametrize(
    "args, expected",
    [
        pytest.param(
            [ConstantObj(value=2, expressions=("2",)), ConstantObj(value=1, expressions=("1",))],
            ("2 1",),
            id="a.insert(10): success case",
        ),
    ],
)
def test_create_expressions(args: list[ExprObj], expected):
    result = InsertExpr._create_expressions(args)

    assert result == expected
