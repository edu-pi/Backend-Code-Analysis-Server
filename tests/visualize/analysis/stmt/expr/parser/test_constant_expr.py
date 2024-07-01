import ast

import pytest

from app.visualize.analysis.stmt.expr.model.expr_obj import ExprObj, ConstantObj
from app.visualize.analysis.stmt.expr.parser.constant_expr import ConstantExpr


@pytest.mark.parametrize(
    "node, expected",
    [
        (ast.Constant(value=10), ConstantObj(value=10, expressions=("10",))),
        (ast.Constant(value="abc"), ConstantObj(value="abc", expressions=("'abc'",))),
    ],
)
def test_parse(node, expected):
    result = ConstantExpr.parse(node)

    assert result == expected


@pytest.mark.parametrize("node, expected", [(ast.Constant(value=10), 10), (ast.Constant(value="abc"), "abc")])
def test_get_literal(node, expected):
    result = ConstantExpr._get_literal(node)

    assert result == expected


@pytest.mark.parametrize("value, expected", [(10, ("10",)), ("abc", ("'abc'",))])
def test_create_expressions(value, expected):
    result = ConstantExpr._create_expressions(value)

    assert result == expected
