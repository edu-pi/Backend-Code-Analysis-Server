import pytest

from app.visualize.analysis.stmt.parser.expr.models.expr_obj import ExprObj, RangeObj, ConstantObj, NameObj
from app.visualize.analysis.stmt.parser.expr.models.range_expression import RangeExpression
from app.visualize.analysis.stmt.parser.expr.parser.built_in_func.range_expr import RangeExpr


@pytest.mark.parametrize(
    "args, expected",
    [
        pytest.param(
            [ConstantObj(value=5, expressions=("5",))],
            RangeObj(value=tuple(range(0, 5, 1)), expressions=(RangeExpression(start="0", end="5", step="1"),)),
            id="range(5): success case",
        ),
        pytest.param(
            [ConstantObj(value=1, expressions=("1",)), ConstantObj(value=5, expressions=("5",))],
            RangeObj(value=tuple(range(1, 5, 1)), expressions=(RangeExpression(start="1", end="5", step="1"),)),
            id="range(1, 5): success case",
        ),
        pytest.param(
            [ConstantObj(value=1, expressions=("1",)), NameObj(value=5, expressions=("a", "5"))],
            RangeObj(
                value=tuple(range(1, 5, 1)),
                expressions=(
                    RangeExpression(start="1", end="a", step="1"),
                    RangeExpression(start="1", end="5", step="1"),
                ),
            ),
            id="range(1, a): success case",
        ),
        pytest.param(
            [
                ConstantObj(value=1, expressions=("1",)),
                ConstantObj(value=5, expressions=("5",)),
                ConstantObj(value=2, expressions=("2",)),
            ],
            RangeObj(value=tuple(range(1, 5, 2)), expressions=(RangeExpression(start="1", end="5", step="2"),)),
            id="range(1, 5, 2): success case",
        ),
    ],
)
def test_parse(mocker, args: list[ExprObj], expected: RangeObj):
    mock_get_value = mocker.patch.object(RangeExpr, "_get_value", return_value=expected.value)
    mock_create_expressions = mocker.patch.object(RangeExpr, "_create_expressions", return_value=expected.expressions)

    result = RangeExpr.parse(args)

    assert isinstance(result, RangeObj)
    assert mock_get_value.called_once_with([arg.value for arg in args])
    assert mock_create_expressions.called_once_with([arg.expressions for arg in args])


@pytest.mark.parametrize(
    "arg_value_list, expected",
    [
        pytest.param(
            [5],
            tuple(range(0, 5, 1)),
            id="range(5): success case",
        ),
        pytest.param(
            [1, 5],
            tuple(range(1, 5, 1)),
            id="range(1, 5): success case",
        ),
        pytest.param(
            [1, 5, 2],
            tuple(range(1, 5, 2)),
            id="range(1, 5, 2): success case",
        ),
    ],
)
def test_get_value(arg_value_list: list, expected):
    result = RangeExpr._get_value(arg_value_list)

    assert result == expected


@pytest.mark.parametrize(
    "args_expressions, expected",
    [
        pytest.param(
            [("5",)],
            (RangeExpression(start="0", end="5", step="1"),),
            id="range(5): success case",
        ),
        pytest.param(
            [("a", "5")],
            (RangeExpression(start="0", end="a", step="1"), RangeExpression(start="0", end="5", step="1")),
            id="range(a): success case",
        ),
        pytest.param(
            [("1",), ("a", "5")],
            (RangeExpression(start="1", end="a", step="1"), RangeExpression(start="1", end="5", step="1")),
            id="range(1, a): success case",
        ),
        pytest.param(
            [("1",), ("a", "5"), ("2",)],
            (RangeExpression(start="1", end="a", step="2"), RangeExpression(start="1", end="5", step="2")),
            id="range(1, a, 2): success case",
        ),
    ],
)
def test_create_expressions(args_expressions: list[tuple], expected):
    result = RangeExpr._create_expressions(args_expressions)

    assert result == expected


@pytest.mark.parametrize(
    "range_list, expected",
    [
        pytest.param(
            [5],
            RangeExpression(start="0", end="5", step="1"),
            id="range(5): success case",
        ),
        pytest.param(
            [1, 5],
            RangeExpression(start="1", end="5", step="1"),
            id="range(1, 5): success case",
        ),
        pytest.param(
            [1, 5, 2],
            RangeExpression(start="1", end="5", step="2"),
            id="range(1, 5, 2): success case",
        ),
    ],
)
def test_make_unit_range_expression(range_list: list, expected):
    result = RangeExpr._make_unit_range_expression(range_list)

    assert result == expected


def test_make_unit_range_expression_fail():
    with pytest.raises(TypeError):
        RangeExpr._make_unit_range_expression([1, 2, 3, 4])
