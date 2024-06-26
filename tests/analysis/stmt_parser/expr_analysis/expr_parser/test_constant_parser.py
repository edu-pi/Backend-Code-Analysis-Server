import ast

import pytest

from app.visualize.analysis.stmt_parser.expr_analysis.expr_models.expr_obj import ExprObj
from app.visualize.analysis.stmt_parser.expr_analysis.expr_parser.constant_parser import ConstantParser


@pytest.mark.parametrize("node, expected", [
    (ast.Constant(value=10), ExprObj(type="constant", value=10, expressions=["10"])),
    (ast.Constant(value="abc"), ExprObj(type="constant", value="abc", expressions=["abc"]))
])
def test_parse(node, expected):
    result = ConstantParser.parse(node)

    assert result == expected


@pytest.mark.parametrize("node, expected", [
    (ast.Constant(value=10), 10),
    (ast.Constant(value="abc"), "abc")
])
def test_get_literal(node, expected):
    result = ConstantParser._get_literal(node)

    assert result == expected


@pytest.mark.parametrize("value, expected", [
    (10, ["10"]),
    ("abc", ["abc"])
])
def test_create_expressions(value, expected):
    result = ConstantParser._create_expressions(value)

    assert result == expected
