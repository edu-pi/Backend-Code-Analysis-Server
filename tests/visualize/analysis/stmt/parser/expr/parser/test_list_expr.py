import pytest

from app.visualize.analysis.stmt.parser.expr.models.expr_obj import ListObj, ExprObj
from app.visualize.analysis.stmt.parser.expr.parser.list_expr import ListExpr


@pytest.mark.parametrize(
    "value, expressions",
    [
        pytest.param([10, 20], ("[10,20]",), id="[10, 20]: success case"),
        pytest.param(
            [11, 20],
            ("[a + 1,20]", "[10 + 1,20]", "[11,20]"),
            id="[a + 1, 20]: success case",
        ),
        pytest.param(
            ["Hello", "World"],
            ("['Hello','World']",),
            id='["Hello", "World"]: success case',
        ),
        pytest.param(
            ["a", "b"],
            ("[a,b]",),
            id="[a, b] success case",
        ),
    ],
)
def test_parse(mocker, value, expressions):
    # _get_value mocking
    mocker.patch("app.visualize.analysis.stmt.parser.expr.parser.list_expr.ListExpr._get_value", return_value=value)
    # _concat_expression mocking
    mocker.patch(
        "app.visualize.analysis.stmt.parser.expr.parser.list_expr.ListExpr._concat_expression",
        return_value=expressions,
    )

    result = ListExpr.parse([mocker.MagicMock(spec=ExprObj) for _ in range(len(value))])

    assert isinstance(result, ListObj)
    assert result.value == value
    assert result.expressions == expressions


@pytest.mark.parametrize(
    "value",
    [
        pytest.param([10, 20], id="[10, 20]: success case"),
        pytest.param([11, 20], id="[11, 20]: success case"),
        pytest.param(["Hello", "World"], id='["Hello", "World"]: success case'),
        pytest.param(["a", "b"], id="[a, b] success case"),
    ],
)
def test_get_value(mocker, value):
    # elts 생성
    elts = [mocker.MagicMock(spec=ExprObj, value=v) for v in value]
    result = ListExpr._get_value(elts)

    assert isinstance(result, list)
    assert result == value


@pytest.mark.parametrize(
    "expressions, transposed_expression_lists_result, expected",
    [
        pytest.param([("10",), ("20",)], [("10", "20")], ("[10,20]",), id="[10, 20]: success case"),
        pytest.param(
            [("a", "10"), ("20",), ("30",)],
            [("a", "20", "30"), ("10", "20", "30")],
            ("[a,20,30]", "[10,20,30]"),
            id="[a, 20, 30]: success case",
        ),
        pytest.param(
            [("a + 1", "10 + 1", "11"), ("20",)],
            [("a + 1", "20"), ("10 + 1", "20"), ("11", "20")],
            ("[a + 1,20]", "[10 + 1,20]", "[11,20]"),
            id="[a + 1, 20]: success case",
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

    result = ListExpr._concat_expression(elts)

    assert result == expected
