import pytest

from app.visualize.analysis.stmt.parser.expr.models.expr_obj import NameObj, BinopObj, ConstantObj, ExprObj
from app.visualize.analysis.stmt.parser.expr.models.expr_type import ExprType
from app.visualize.analysis.stmt.parser.expr.parser.formatted_value_expr import FormattedValueExpr


@pytest.mark.parametrize(
    "expr_obj, conversion, format_spec, expected",
    [
        pytest.param(
            ConstantObj(value=10, expressions=("10",)),
            -1,
            None,
            10,
            id="{a}: success case",
        ),
        pytest.param(
            NameObj(value=10, expressions=("a", "10"), type=ExprType.VARIABLE),
            -1,
            None,
            10,
            id="{a}: success case",
        ),
        pytest.param(
            BinopObj(value=50, expressions=("x + y", "30 + 20", "50")),
            -1,
            None,
            50,
            id="{x + y}: success case",
        ),
    ],
)
def test_get_value(expr_obj: ExprObj, conversion, format_spec, expected):
    result = FormattedValueExpr._get_value(expr_obj, conversion, format_spec)
    assert result == expected


@pytest.mark.parametrize(
    "expr_obj, conversion, format_spec, expected",
    [
        pytest.param(
            ConstantObj(value=10, expressions=("10",)),
            -1,
            None,
            ("10",),
            id="{a}: success case",
        ),
        pytest.param(
            NameObj(value=10, expressions=("a", "10"), type=ExprType.VARIABLE),
            -1,
            None,
            ("{a}", "10"),
            id="{a}: success case",
        ),
        pytest.param(
            BinopObj(value=50, expressions=("x + y", "30 + 20", "50")),
            -1,
            None,
            ("{x + y}", "{30 + 20}", "50"),
            id="{x + y}: success case",
        ),
    ],
)
def test_concat_expression(expr_obj: ExprObj, conversion, format_spec, expected):
    result = FormattedValueExpr._concat_expressions(expr_obj, conversion, format_spec)

    assert result == expected
