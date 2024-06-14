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


# 테스트 데이터를 별도의 변수에 저장
test_data = [
    (ast.Call(func=ast.Name(id='print', ctx=ast.Load()), args=[], keywords=[]), 'print', True),
    (ast.Call(func=ast.Name(id='range', ctx=ast.Load()), args=[], keywords=[]), 'range', True),
    (ast.Call(func=ast.Name(id='print', ctx=ast.Load()), args=[], keywords=[]), '', False),
    (ast.Call(func=ast.Name(id='range', ctx=ast.Load()), args=[], keywords=[]), 'print', False),
]


@pytest.mark.parametrize("node, expect, success", test_data)
def test_get_func_name(call_parser, node, expect, success):
    """
    ast.Call 노드가 주어졌을 때 함수 아이디를 제대로 가져오는지 테스트
    :param node: ast.Call 노드
    :param expect: 예상되는 함수 아이디
    :param success: 테스트가 성공해야 하는지 (True), 실패해야 하는지 (False)
    :return: None
    """
    parser = call_parser(node)
    result = parser._CallParser__get_func_name()
    if success:
        assert result == expect
    else:
        assert result != expect