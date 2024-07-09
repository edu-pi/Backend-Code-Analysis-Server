# _*_ coding: utf-8 _*_

import pytest

from app.visualize.analysis.stmt.parser.expr.models.expr_obj import ListObj, ConstantObj, BinopObj, NameObj, ExprObj
from app.visualize.analysis.stmt.parser.expr.parser.list_expr import ListExpr


@pytest.mark.parametrize(
    "elts, expected",
    [
        pytest.param(
            [ConstantObj(value=10, expressions=("10",)), ConstantObj(value=20, expressions=("20",))],
            ListObj(value=[10, 20], expressions=("[10,20]",)),
            id="[10, 20]: success case",
        ),
        pytest.param(
            [BinopObj(value=11, expressions=("a + 1", "10 + 1", "11")), ConstantObj(value=20, expressions=("20",))],
            ListObj(value=[11, 20], expressions=("[a + 1,20]", "[10 + 1,20]", "[11,20]")),
            id="[a + 1, 20]: success case",
        ),
        pytest.param(
            [
                ConstantObj(value="Hello", expressions=("'Hello'",)),
                ConstantObj(value="World", expressions=("'World'",)),
            ],
            ListObj(value=["Hello", "World"], expressions=("['Hello','World']",)),
            id='["Hello", "World"]: success case',
        ),
        pytest.param(
            [NameObj(value="a", expressions=("a",)), NameObj(value="b", expressions=("b",))],
            ListObj(value=["a", "b"], expressions=("[a,b]",)),
            id="[a, b] success case",
        ),
    ],
)
def test_parse(elts: list[ExprObj], expected):
    result = ListExpr.parse(elts)

    assert result == expected
