from unittest.mock import MagicMock

import pytest

from app.visualize.analysis.stmt.parser.expr.models.expr_obj import (
    AttributeObj,
    ExprObj,
    PopObj,
)
from app.visualize.analysis.stmt.parser.expr.models.expr_type import ExprType
from app.visualize.analysis.stmt.parser.expr.parser.attr_func.pop_expr import PopExpr


@pytest.mark.parametrize(
    "elem_container_dict, expressions, args, expected",
    [
        pytest.param(
            {"a": [1, 2, 3, 4, 5]},
            ("a", "[1, 2, 3, 4, 5]"),
            [],
            PopObj(value="a", expressions=("5",)),
            id="a.pop(): success case",
        ),
    ],
)
def test_parse(mocker, elem_container_dict: dict, expressions: tuple, args: list[ExprObj], expected: AttributeObj):
    mock_pop_value = mocker.patch.object(PopExpr, "_pop_value", return_value=expected.value)
    mock_get_value = mocker.patch.object(PopExpr, "_get_value", return_value=expected.value)
    mock_create_expressions = mocker.patch.object(PopExpr, "_create_expressions", return_value=expected.expressions)

    attr_obj = AttributeObj(
        value=getattr(elem_container_dict["a"], "pop"),
        expressions=expressions,
        type=ExprType.POP,
    )

    result = PopExpr.parse(attr_obj, args)

    assert isinstance(result, PopObj)
    mock_pop_value.assert_called_once_with(attr_obj)
    mock_get_value.assert_called_once_with(attr_obj)
    mock_create_expressions.assert_called_once()


def test_parse_wrong_arguments():
    attr_obj = MagicMock(spec=AttributeObj)
    args = [MagicMock(spec=ExprObj), MagicMock(spec=ExprObj)]

    with pytest.raises(ValueError):
        PopExpr.parse(attr_obj, args)


@pytest.mark.parametrize(
    "elem_container_dict, expressions",
    [
        pytest.param(
            {"a": [1, 2, 3, 4, 5]},
            ("a", "[1, 2, 3, 4, 5]"),
            id="a.pop(): success case",
        ),
    ],
)
def test_pop_value(elem_container_dict: dict, expressions: tuple):
    attr_obj = AttributeObj(
        value=getattr(elem_container_dict["a"], "pop"),
        expressions=expressions,
        type=ExprType.POP,
    )
    result = PopExpr._pop_value(attr_obj)

    assert result == 5
    assert elem_container_dict["a"] == [1, 2, 3, 4]


@pytest.mark.parametrize(
    "elem_container_dict, expressions, expected",
    [
        pytest.param(
            {"a": [1, 2, 3, 4, 5]},
            ("a", "[1, 2, 3, 4, 5]"),
            "a",
            id="a.pop(): success case",
        )
    ],
)
def test_get_value(elem_container_dict: dict, expressions: tuple, expected: str):
    attr_obj = AttributeObj(
        value=getattr(elem_container_dict["a"], "pop"),
        expressions=expressions,
        type=ExprType.POP,
    )
    result = PopExpr._get_value(attr_obj)

    assert result == expected


@pytest.mark.parametrize(
    "target, return_value, expected",
    [
        pytest.param(
            "a",
            5,
            ("a", "5"),
            id="a.pop(): success case",
        ),
    ],
)
def test_create_expressions(target, return_value, expected):
    result = PopExpr._create_expressions(target, return_value)

    assert result == expected
