import pytest
import ast
from unittest.mock import MagicMock, patch
from app.analysis.generator.parser.name_parser import NameParser, Name
from app.analysis.element_manager import CodeElementManager


@pytest.fixture
def elem_manager():
    mock = MagicMock(spec=CodeElementManager)
    mock.get_variable_value.return_value = 10
    return mock


@pytest.fixture
def name_parser(elem_manager):
    # NameParser 인스턴스를 생성하는 함수를 반환
    def _create_parser(node):
        return NameParser(node, elem_manager)

    return _create_parser


@pytest.fixture
def create_ast_name_node():
    # 코드를 ast.Name 노드로 변환하는 함수를 반환
    def _create_ast_name_node(name_id, ctx):
        # ast.Name 반환
        return ast.Name(id=name_id, ctx=ctx)

    return _create_ast_name_node


@pytest.mark.parametrize("name_id, ctx, expect_value, expect_expressions", [
    ("abc", ast.Store(), None, None),
    ("b", ast.Load(), 10, ['b', '10'])
])
def test_parse(create_ast_name_node, name_parser, name_id, ctx, expect_value, expect_expressions):
    """
    ast.Name 노드가 주어졌을 때 Name 인스턴스를 생성하는지 테스트
    """
    name_node = create_ast_name_node(name_id, ctx)
    expect = Name(name_id, expect_value, expect_expressions)

    with patch.object(NameParser, '_NameParser__get_value', return_value=expect_value), \
            patch.object(NameParser, '_NameParser__get_expressions', return_value=expect_expressions):
        parser = name_parser(name_node)
        result = parser.parse()

        assert result == expect


@pytest.mark.parametrize("name_id, ctx, expect", [
    ("b", ast.Load(), 10)
])
def test__get_value(create_ast_name_node, name_parser, name_id, ctx, expect):
    """
    ast.Name 노드가 주어졌을 때 value를 가져오는지 테스트
    """
    name_node = create_ast_name_node(name_id, ctx)
    parser = name_parser(name_node)
    result = parser._NameParser__get_value()

    assert result == expect


@pytest.mark.parametrize("name_id, value, ctx, expect", [
    ("b", 10, ast.Load(), ['b', '10'])
])
def test__get_expressions(create_ast_name_node, name_parser, name_id, value, ctx, expect):
    """
    ast.Name 노드가 주어졌을 때 value를 가져오는지 테스트
    """
    name_node = create_ast_name_node(name_id, ctx)
    parser = name_parser(name_node)
    result = parser._NameParser__get_expressions(value)

    assert result == expect
