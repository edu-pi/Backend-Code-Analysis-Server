from unittest.mock import MagicMock

import pytest

from app.visualize.analysis.stmt.parser.expr.models.expr_obj import (
    AttributeObj,
    ExprObj,
    ConstantObj,
    NameObj,
    RemoveObj,
    BinopObj,
)
from app.visualize.analysis.stmt.parser.expr.models.expr_type import ExprType
from app.visualize.analysis.stmt.parser.expr.parser.attr_func.remove_expr import RemoveExpr


@pytest.mark.parametrize(
    "elem_container_dict, expressions, args, expected",
    [
        pytest.param(
            {"a": [1, 2, 3, 4, 5]},
            ("a", "[1, 2, 3, 4, 5]"),
            [ConstantObj(value=0, expressions=("0",))],
            RemoveObj(value="a", expressions=("0",)),
            id="a.remove(0): success case",
        ),
        pytest.param(
            {"a": [1, 2, 3, 4, 5]},
            ("a", "[1, 2, 3, 4, 5]"),
            [BinopObj(value=2, expressions=("b + 1", "1 + 1", "2"))],
            RemoveObj(value="a", expressions=("b + 1", "1 + 1", "2")),
            id="a.remove(b + 1): success case",
        ),
    ],
)
def test_parse(mocker, elem_container_dict: dict, expressions: tuple, args: list[ExprObj], expected: AttributeObj):
    mock_remove_value = mocker.patch.object(RemoveExpr, "_remove_value", return_value=expected.value)
    mock_get_value = mocker.patch.object(RemoveExpr, "_get_value", return_value=expected.value)
    mock_create_expressions = mocker.patch.object(RemoveExpr, "_create_expressions", return_value=expected.expressions)

    attr_obj = AttributeObj(
        value=getattr(elem_container_dict["a"], "remove"),
        expressions=expressions,
        type=ExprType.REMOVE,
    )

    result = RemoveExpr.parse(attr_obj, args)

    assert isinstance(result, RemoveObj)
    mock_remove_value.assert_called_once_with(attr_obj, args[0])
    mock_get_value.assert_called_once_with(attr_obj)
    mock_create_expressions.assert_called_once_with(args[0])


def test_parse_wrong_arguments():
    attr_obj = MagicMock(spec=AttributeObj)
    args = [MagicMock(spec=ExprObj), MagicMock(spec=ExprObj)]

    with pytest.raises(ValueError):
        RemoveExpr.parse(attr_obj, args)


@pytest.mark.parametrize(
    "elem_container_dict, expressions, arg",
    [
        pytest.param(
            {"a": [1, 2, 3, 4, 5]},
            ("a", "[1, 2, 3, 4, 5]"),
            ConstantObj(value=2, expressions=("2",)),
            id="a.remove(2): success case",
        ),
        pytest.param(
            {"a": [1, 2, 3, 4, 5]},
            ("a", "[1, 2, 3, 4, 5]"),
            BinopObj(value=2, expressions=("b + 1", "1 + 1", "2")),
            id="a.remove(b + 1): success case",
        ),
    ],
)
def test_remove_value(elem_container_dict: dict, expressions: tuple, arg: ExprObj):
    attr_obj = AttributeObj(
        value=getattr(elem_container_dict["a"], "remove"),
        expressions=expressions,
        type=ExprType.REMOVE,
    )
    RemoveExpr._remove_value(attr_obj, arg)

    assert elem_container_dict["a"] == [1, 3, 4, 5]


@pytest.mark.parametrize(
    "elem_container_dict, expressions, expected",
    [
        pytest.param(
            {"a": [1, 2, 3, 4, 5]},
            ("a", "[1, 2, 3, 4, 5]"),
            "a",
            id="a.remove(0): success case",
        )
    ],
)
def test_get_value(elem_container_dict: dict, expressions: tuple, expected: str):
    attr_obj = AttributeObj(
        value=getattr(elem_container_dict["a"], "remove"),
        expressions=expressions,
        type=ExprType.REMOVE,
    )
    result = RemoveExpr._get_value(attr_obj)

    assert result == expected


@pytest.mark.parametrize(
    "arg, expected",
    [
        pytest.param(
            ConstantObj(value=10, expressions=("10",)),
            ("10",),
            id="a.remove(10): success case",
        ),
        pytest.param(
            NameObj(value=11, expressions=("b + 1", "10 + 1", "11"), type=ExprType.VARIABLE),
            ("b + 1", "10 + 1", "11"),
            id="a.remove(b + 1): success case",
        ),
    ],
)
def test_create_expressions(arg: ExprObj, expected):
    result = RemoveExpr._create_expressions(arg)

    assert result == expected
