from unittest.mock import MagicMock, patch

import ast
import pytest

from app.analysis.generator.for_generator import ForGenerator
from app.analysis.generator.parser.call_parser import NameParser
from app.analysis.element_manager import CodeElementManager
from tests.analysis.generator.parser.test_data.for_generator_data import data__get_identifier

@pytest.fixture
def create_ast_node():
    # 코드를 ast 노드로 변환하는 함수를 반환
    def _create_ast_node(code):
        # ast.Call 반환
        return ast.parse(code).body[0]

    return _create_ast_node

@pytest.fixture
def elem_manager():
    mock = MagicMock(spec=CodeElementManager)
    mock.return_value.get_call_id.return_value = 5
    return mock


@pytest.fixture
def for_generator(elem_manager):
    # ForGenerator 인스턴스를 생성하는 함수를 반환
    def _create_generator(node):
        return ForGenerator(node, elem_manager)

    return _create_generator


@pytest.mark.parametrize("node, expect", [
    ('''for i in range(3): \n    pass''', [3]),
    ('''for i in range(1,5,2): \n    pass''', [1, 5, 2]),
    ('''for i in range(1,a): \n    pass''', [1, 5])
])
def test___get_identifiers(for_generator, create_ast_node, node, expect):
    """ast.For 노드가 주어졌을 때 __get_identifiers 메서드가 정상적으로 동작하는지 테스트"""
    generator = for_generator(create_ast_node(node))
    with patch.object(NameParser, 'parse', return_value=ast.Name(id='a', value=5, expressions=['a', '5'])):
        actual = generator._ForGenerator__get_identifiers()

        assert actual == expect


@pytest.mark.parametrize("node", [
    '''for i in list(a): \n    pass''',
    '''for i in a: \n    pass''',
])
def test___get_identifiers_fail(for_generator, create_ast_node, node):
    """ast.For 노드가 주어졌을 때 __get_identifiers 메서드가 에외를 발생하는지 테스트"""
    generator = for_generator(create_ast_node(node))
    with patch.object(NameParser, 'parse', return_value=ast.Name(id='a', value=5, expressions=['a', '5'])):
        with pytest.raises(TypeError):
            generator._ForGenerator__get_identifiers()

