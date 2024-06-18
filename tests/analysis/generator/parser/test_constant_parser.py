import ast
from unittest.mock import patch

import pytest

from app.analysis.generator.parser.constant_parser import ConstantParser, Constant


@pytest.mark.parametrize("value, expect", [
    (10, Constant(value=10, expressions=["10"])),
    ("abc_abc", Constant(value="abc_abc", expressions=["abc_abc"])),
    ("abcAbc", Constant(value="abcAbc", expressions=["abcAbc"]))
])
def test_parse(value, expect):
    constant = ast.Constant(value=value)
    with patch.object(ConstantParser, '_ConstantParser__get_value', return_value=value), \
            patch.object(ConstantParser, '_ConstantParser__get_expressions', return_value=[str(value)]):
        result = ConstantParser.parse(constant)
        assert result == expect


@pytest.mark.parametrize("value, expect", [
    (10, 10),
    ("abc_abc", "abc_abc"),
    ("abcAbc", "abcAbc")
])
def test__get_value(value, expect):
    constant = ast.Constant(value=value)
    constant_parser = ConstantParser(constant)

    result = constant_parser._ConstantParser__get_value()

    assert result == expect


@pytest.mark.parametrize("value, expect", [
    (10, ["10"]),
    ("abc_abc", ["abc_abc"]),
    ("abcAbc", ["abcAbc"])
])
def test__get_expressions(value, expect):
    constant = ast.Constant(value=value)
    constant_parser = ConstantParser(constant)

    result = constant_parser._ConstantParser__get_expressions()

    assert result == expect
