import pytest

from app.visualize.analysis.stmt.parser.expr.models.expr_obj import TupleObj, ExprObj, ConstantObj, NameObj, BinopObj
from app.visualize.analysis.stmt.parser.expr.parser.tuple_expr import TupleExpr


@pytest.mark.parametrize(
    "elts, expected",
    [
        pytest.param(
            [ConstantObj(value=10, expressions=("10",)), ConstantObj(value=20, expressions=("20",))],
            TupleObj(value=(10, 20), expressions=("[10,20]",)),
            id="(10, 20): success case",
        ),
        pytest.param(
            [BinopObj(value=11, expressions=("a + 1", "10 + 1", "11")), ConstantObj(value=20, expressions=("20",))],
            TupleObj(value=(11, 20), expressions=("[a + 1,20]", "[10 + 1,20]", "[11,20]")),
            id="(a + 1, 20): success case",
        ),
        pytest.param(
            [NameObj(value="Hello", expressions=("a", "Hello")), ConstantObj(value="World", expressions=("World",))],
            TupleObj(value=("Hello", "World"), expressions=("['a','World']", "['Hello','World']")),
            id='(a, "World"): success case',
        ),
    ],
)
def test_parse(mocker, elts: list[ExprObj], expected: TupleObj):
    mock_get_value = mocker.patch.object(TupleExpr, "_get_value", return_value=expected.value)
    mock_concat_expressions = mocker.patch.object(TupleExpr, "_concat_expressions", return_value=expected.expressions)

    result = TupleExpr.parse(elts)

    assert isinstance(result, TupleObj)
    assert mock_get_value.call_once_with(elts)
    assert mock_concat_expressions.call_once_with(elts)


@pytest.mark.parametrize(
    "expected",
    [
        pytest.param((10, 20), id="(10, 20): success case"),
        pytest.param((11, 20), id="(11, 20): success case"),
        pytest.param(("Hello", "World"), id='("Hello", "World"): success case'),
        pytest.param(("a", "b"), id="(a, b) success case"),
    ],
)
def test_get_value(mocker, expected):
    # elts 생성
    elts = [mocker.MagicMock(spec=ExprObj, value=v) for v in expected]
    result = TupleExpr._get_value(elts)

    assert isinstance(result, tuple)
    assert result == expected


@pytest.mark.parametrize(
    "expressions, transposed_expression_lists_result, expected",
    [
        pytest.param([("10",), ("20",)], [("10", "20")], ("(10, 20)",), id="(10, 20): success case"),
        pytest.param(
            [("a", "10"), ("20",), ("30",)],
            [("a", "20", "30"), ("10", "20", "30")],
            ("(a, 20, 30)", "(10, 20, 30)"),
            id="(a, 20, 30): success case",
        ),
        pytest.param(
            [("a + 1", "10 + 1", "11"), ("20",)],
            [("a + 1", "20"), ("10 + 1", "20"), ("11", "20")],
            ("(a + 1, 20)", "(10 + 1, 20)", "(11, 20)"),
            id="(a + 1, 20): success case",
        ),
    ],
)
def test_concat_expression(mocker, expressions, transposed_expression_lists_result, expected):
    # elts 생성
    elts = [mocker.MagicMock(spec=ExprObj, expressions=expr) for expr in expressions]
    mocker.patch(
        "app.visualize.utils.utils.transpose_with_last_fill",
        return_value=transposed_expression_lists_result,
    )

    result = TupleExpr._concat_expressions(elts)

    assert result == expected
