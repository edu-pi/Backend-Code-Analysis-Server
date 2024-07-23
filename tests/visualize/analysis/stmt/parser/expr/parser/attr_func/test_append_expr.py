from unittest.mock import MagicMock

import pytest

from app.visualize.analysis.stmt.parser.expr.models.expr_obj import (
    AttributeObj,
    ExprObj,
    ConstantObj,
    NameObj,
    AppendObj,
)
from app.visualize.analysis.stmt.parser.expr.models.expr_type import ExprType
from app.visualize.analysis.stmt.parser.expr.parser.attr_func.append_expr import AppendExpr


@pytest.mark.parametrize(
    "elem_container_dict, expressions, args, expected",
    [
        pytest.param(
            {"a": [1, 2, 3, 4, 5]},
            ("a", "[1, 2, 3, 4, 5]"),
            [ConstantObj(value=10, expressions=("10",))],
            AppendObj(value="a", expressions=("10",)),
            id="a.append(10): success case",
        ),
        pytest.param(
            {"a": [1, 2, 3, 4, 5]},
            ("a", "[1, 2, 3, 4, 5]"),
            [ConstantObj(value=10, expressions=("b + 1", "10 + 1", "11"))],
            AppendObj(value="a", expressions=("b + 1", "10 + 1", "11")),
            id="a.append(b + 1): success case",
        ),
    ],
)
def test_parse(mocker, elem_container_dict: dict, expressions: tuple, args: list[ExprObj], expected: AttributeObj):
    mock_get_value = mocker.patch.object(AppendExpr, "_get_value", return_value=expected.value)
    mock_create_expressions = mocker.patch.object(AppendExpr, "_create_expressions", return_value=expected.expressions)

    attr_obj = AttributeObj(
        value=getattr(elem_container_dict["a"], "append"),
        expressions=expressions,
        type=ExprType.APPEND,
    )

    result = AppendExpr.parse(attr_obj, args)

    assert isinstance(result, AppendObj)
    mock_get_value.assert_called_once_with(attr_obj)
    mock_create_expressions.assert_called_once_with(args[0])


def test_parse_wrong_arguments():
    attr_obj = MagicMock(spec=AttributeObj)
    args = [MagicMock(spec=ExprObj), MagicMock(spec=ExprObj)]

    with pytest.raises(ValueError):
        AppendExpr.parse(attr_obj, args)


@pytest.mark.parametrize(
    "elem_container_dict, expressions, arg",
    [
        pytest.param(
            {"a": [1, 2, 3, 4, 5]},
            ("a", "[1, 2, 3, 4, 5]"),
            ConstantObj(value=10, expressions=("10",)),
            id="a.append(10): success case",
        ),
        pytest.param(
            {"a": [1, 2, 3, 4, 5]},
            ("a", "[1, 2, 3, 4, 5]"),
            NameObj(value=11, expressions=("b + 1", "10 + 1", "11"), type=ExprType.VARIABLE),
            id="a.append(b + 1): success case",
        ),
    ],
)
def test_append_value(elem_container_dict: dict, expressions: tuple, arg: ExprObj):
    attr_obj = AttributeObj(
        value=getattr(elem_container_dict["a"], "append"),
        expressions=expressions,
        type=ExprType.APPEND,
    )
    AppendExpr._append_value(attr_obj, arg)

    assert elem_container_dict["a"] == [1, 2, 3, 4, 5, arg.value]


@pytest.mark.parametrize(
    "elem_container_dict, expressions, expected",
    [
        pytest.param(
            {"a": [1, 2, 3, 4, 5]},
            ("a", "[1, 2, 3, 4, 5]"),
            "a",
            id="a.append(10): success case",
        )
    ],
)
def test_get_value(elem_container_dict: dict, expressions: tuple, expected: str):
    attr_obj = AttributeObj(
        value=getattr(elem_container_dict["a"], "append"),
        expressions=expressions,
        type=ExprType.APPEND,
    )
    result = AppendExpr._get_value(attr_obj)

    assert result == expected


@pytest.mark.parametrize(
    "arg, expected",
    [
        pytest.param(
            ConstantObj(value=10, expressions=("10",)),
            ("10",),
            id="a.append(10): success case",
        ),
        pytest.param(
            NameObj(value=11, expressions=("b + 1", "10 + 1", "11"), type=ExprType.VARIABLE),
            ("b + 1", "10 + 1", "11"),
            id="a.append(b + 1): success case",
        ),
    ],
)
def test_create_expressions(arg: ExprObj, expected):
    result = AppendExpr._create_expressions(arg)

    assert result == expected
