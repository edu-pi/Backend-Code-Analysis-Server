import ast

import pytest

from app.visualize.analysis.stmt.expr.model.expr_obj import ListObj, ConstantObj, BinopObj, NameObj
from app.visualize.analysis.stmt.expr.parser.list_expr import ListExpr


@pytest.mark.parametrize(
    "elts, expected",
    [
        pytest.param(
            [ConstantObj(value=10, expressions=("10",)), ConstantObj(value=20, expressions=("20",))],
            ListObj(value=(10, 20), expressions=("[10,20]",)),
            id="[10, 20] 배열이 들어오는 경우",
        ),
        pytest.param(
            [BinopObj(value=11, expressions=("a + 1", "10 + 1", "11")), ConstantObj(value=20, expressions=("20",))],
            ListObj(value=(11, 20), expressions=("[a + 1,20]", "[10 + 1,20]", "[11,20]")),
            id="[a + 1, 20] 배열이 들어오는 경우",
        ),
        pytest.param(
            [
                ConstantObj(value="Hello", expressions=("'Hello'",)),
                ConstantObj(value="World", expressions=("'World'",)),
            ],
            ListObj(value=("Hello", "World"), expressions=("['Hello','World']",)),
            id='["Hello", "World"] 배열이 들어오는 경우',
        ),
        pytest.param(
            [NameObj(value="a", expressions=("a",)), NameObj(value="b", expressions=("b",))],
            ListObj(value=("a", "b"), expressions=("[a,b]",)),
            id="[a, b] 배열이 들어오는 경우",
        ),
    ],
)
def test_parse(elts, expected):
    result = ListExpr.parse(elts)

    assert result == expected
