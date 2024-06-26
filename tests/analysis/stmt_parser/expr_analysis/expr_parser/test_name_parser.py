import ast

import pytest

from app.visualize.analysis.stmt_parser.expr_analysis.expr_models.expr_obj import ExprObj
from app.visualize.analysis.stmt_parser.expr_analysis.expr_parser.name_parser import NameParser


@pytest.mark.parametrize("ctx, identifier_name, expected", [
    (ast.Store(), "a", ExprObj(type="name", value="a", expressions=["a"])),
    (ast.Store(), "abc", ExprObj(type="name", value="abc", expressions=["abc"])),
    (ast.Load(), "a", ExprObj(type="name", value=10, expressions=["a", "10"])),
    (ast.Load(), "abc", ExprObj(type="name", value=10, expressions=["abc", "10"])),
])
def test_parse(elem_manager, ctx, identifier_name, expected):
    result = NameParser.parse(ctx, identifier_name, elem_manager)

    assert result == expected


@pytest.mark.parametrize("identifier, expected", [
    ("a", 10),
    ("abc", 10)
])
def test_get_identifier_value(elem_manager, identifier, expected):
    result = NameParser._get_identifier_value(identifier, elem_manager)

    assert result == expected


@pytest.mark.parametrize("identifier_name, value, expected", [
    ("a", 10, ["a", "10"]),
    ("abc", 10, ["abc", "10"])
])
def test_create_expressions(identifier_name, value, expected):
    result = NameParser._create_expressions(identifier_name, value)

    assert result == expected
