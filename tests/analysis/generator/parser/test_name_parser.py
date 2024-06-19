import pytest
import ast
from unittest.mock import patch
from app.analysis.generator.parser.name_parser import NameParser, Name


@pytest.mark.parametrize("name_id, ctx, expect_value, expect_expressions", [
    ("abc", ast.Store(), None, None),
    ("b", ast.Load(), 10, ['b', '10'])
])
def test_parse(elem_manager, name_id, ctx, expect_value, expect_expressions):
    """
    ast.Name 노드가 주어졌을 때 Name 인스턴스를 생성하는지 테스트
    """
    name_node = ast.Name(id=name_id, ctx=ctx)
    expect = Name(name_id, expect_value, expect_expressions)

    with patch.object(NameParser, '_NameParser__get_value', return_value=expect_value), \
            patch.object(NameParser, '_NameParser__get_expressions', return_value=expect_expressions):
        result = NameParser.parse(name_node, elem_manager)

        assert result == expect


@pytest.mark.parametrize("name_id, ctx, expect", [
    ("b", ast.Load(), 10),
    ("abc_abc", ast.Load(), 10),
    ("abcAbc", ast.Load(), 10)
])
def test__get_value(elem_manager, name_id, ctx, expect):
    """
    ast.Name 노드가 주어졌을 때 value를 가져오는지 테스트
    """

    name_node = ast.Name(id=name_id, ctx=ctx)
    name_parser = NameParser(name_node, elem_manager)

    result = name_parser._NameParser__get_value()

    assert result == expect


@pytest.mark.parametrize("name_id, value, ctx, expect", [
    ("b", 10, ast.Load(), ['b', '10']),
    ("abc_abc", 10, ast.Load(), ['abc_abc', '10']),
    ("abcAbc", 10, ast.Load(), ['abcAbc', '10'])
])
def test__get_expressions(elem_manager, name_id, value, ctx, expect):
    """
    ast.Name 노드가 주어졌을 때 value를 가져오는지 테스트
    """

    name_node = ast.Name(id=name_id, ctx=ctx)
    name_parser = NameParser(name_node, elem_manager)

    result = name_parser._NameParser__get_expressions(value)

    assert result == expect
