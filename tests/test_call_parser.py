from unittest.mock import MagicMock

import ast
import pytest

from app.analysis.generator.parser.call_parser import CallParser
from app.analysis.element_manager import CodeElementManager

@pytest.fixture
def elem_manager():
    """Fixture to create a CodeElementManager instance."""
    return MagicMock(spec=CodeElementManager)


@pytest.fixture
def call_parser(elem_manager):
    # CallParser 인스턴스를 생성하는 함수를 반환
    def _create_parser(node):
        return CallParser(node, elem_manager)
    return _create_parser


@pytest.mark.parametrize(
    "node, expect",
    [
        (ast.Call(func=ast.Name(id='print', ctx=ast.Load()), args=[], keywords=[]), 'print'),
        (ast.Call(func=ast.Name(id='range', ctx=ast.Load()), args=[], keywords=[]), 'range'),
    ]
)
def test_get_func_name(call_parser, node, expect):
    """
    ast.Call 노드가 주어졌을 때 함수 아이디를 제대로 가져오는지 테스트
    :param node: ast.Call 노드
    :param expect: 예상되는 함수 아이디
    :return: None
    """
    parser = call_parser(node)
    result = parser._CallParser__get_func_name()
    assert result == expect
