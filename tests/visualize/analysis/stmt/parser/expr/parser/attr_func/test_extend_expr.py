from unittest.mock import MagicMock

import pytest

from app.visualize.analysis.stmt.parser.expr.models.expr_obj import (
    AttributeObj,
    ExprObj,
    NameObj,
    ExtendObj,
    ListObj,
)
from app.visualize.analysis.stmt.parser.expr.models.expr_type import ExprType
from app.visualize.analysis.stmt.parser.expr.parser.attr_func.extend_expr import ExtendExpr


@pytest.mark.parametrize(
    "elem_container_dict, expressions, args, expected",
    [
        pytest.param(
            {"a": [1, 2, 3, 4, 5]},
            ("a", "[1, 2, 3, 4, 5]"),
            [ListObj(value=[10, 20], expressions=("[10, 20]",))],
            ExtendObj(value="a", expressions=("[10, 20]",)),
            id="a.extend([10, 20]): success case",
        ),
        pytest.param(
            {"a": [1, 2, 3, 4, 5]},
            ("a", "[1, 2, 3, 4, 5]"),
            [NameObj(value=[10, 20], expressions=("b", "[10, 20]"), type=ExprType.LIST)],
            ExtendObj(value="a", expressions=("b", "[10, 20]")),
            id="a.extend(b): success case",
        ),
    ],
)
def test_parse(mocker, elem_container_dict: dict, expressions: tuple, args: list[ExprObj], expected: AttributeObj):
    mock_extend_value = mocker.patch.object(ExtendExpr, "_extend_value", return_value=expected.value)
    mock_get_value = mocker.patch.object(ExtendExpr, "_get_value", return_value=expected.value)
    mock_create_expressions = mocker.patch.object(ExtendExpr, "_create_expressions", return_value=expected.expressions)

    attr_obj = AttributeObj(
        value=getattr(elem_container_dict["a"], "extend"),
        expressions=expressions,
        type=ExprType.EXTEND,
    )

    result = ExtendExpr.parse(attr_obj, args)

    assert isinstance(result, ExtendObj)
    mock_extend_value.assert_called_once_with(attr_obj, args[0])
    mock_get_value.assert_called_once_with(attr_obj)
    mock_create_expressions.assert_called_once_with(args[0])


def test_parse_wrong_arguments():
    attr_obj = MagicMock(spec=AttributeObj)
    args = [MagicMock(spec=ExprObj), MagicMock(spec=ExprObj)]

    with pytest.raises(ValueError):
        ExtendExpr.parse(attr_obj, args)


@pytest.mark.parametrize(
    "elem_container_dict, expressions, arg",
    [
        pytest.param(
            {"a": [1, 2, 3, 4, 5]},
            ("a", "[1, 2, 3, 4, 5]"),
            ListObj(value=[10, 20], expressions=("[10, 20]",)),
            id="a.extend([10, 20]): success case",
        ),
        pytest.param(
            {"a": [1, 2, 3, 4, 5]},
            ("a", "[1, 2, 3, 4, 5]"),
            NameObj(value=[10, 20], expressions=("b", "[10, 20]"), type=ExprType.LIST),
            id="a.extend(b): success case",
        ),
    ],
)
def test_extend_value(elem_container_dict: dict, expressions: tuple, arg: ExprObj):
    attr_obj = AttributeObj(
        value=getattr(elem_container_dict["a"], "extend"),
        expressions=expressions,
        type=ExprType.EXTEND,
    )
    ExtendExpr._extend_value(attr_obj, arg)

    assert elem_container_dict["a"] == [1, 2, 3, 4, 5, 10, 20]


@pytest.mark.parametrize(
    "elem_container_dict, expressions, expected",
    [
        pytest.param(
            {"a": [1, 2, 3, 4, 5]},
            ("a", "[1, 2, 3, 4, 5]"),
            "a",
            id="a.extend(0): success case",
        )
    ],
)
def test_get_value(elem_container_dict: dict, expressions: tuple, expected: str):
    attr_obj = AttributeObj(
        value=getattr(elem_container_dict["a"], "extend"),
        expressions=expressions,
        type=ExprType.EXTEND,
    )
    result = ExtendExpr._get_value(attr_obj)

    assert result == expected


@pytest.mark.parametrize(
    "arg, expected",
    [
        pytest.param(
            ListObj(value=[10, 20], expressions=("[10, 20]",)),
            ("[10, 20]",),
            id="a.extend(10): success case",
        ),
        pytest.param(
            NameObj(value=[10, 20], expressions=("b", "[10, 20]"), type=ExprType.LIST),
            ("b", "[10, 20]"),
            id="a.extend(b): success case",
        ),
    ],
)
def test_create_expressions(arg: ExprObj, expected):
    result = ExtendExpr._create_expressions(arg)

    assert result == expected
