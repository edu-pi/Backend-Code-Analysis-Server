from unittest.mock import MagicMock, patch

import ast
import pytest

from app.analysis.generator.parser.call_parser import CallParser, Print
from app.analysis.element_manager import CodeElementManager


@pytest.fixture
def elem_manager():
    """Fixture to create a CodeElementManager instance."""
    mock = MagicMock(spec=CodeElementManager)
    mock.get_variable_value.return_value = 1
    return mock


@pytest.fixture
def call_parser(elem_manager):
    # CallParser 인스턴스를 생성하는 함수를 반환
    def _create_parser(node):
        return CallParser(node, elem_manager)

    return _create_parser


@pytest.fixture
def create_ast_node():
    # 코드를 ast 노드로 변환하는 함수를 반환
    def _create_ast_node(code):
        # ast.Call 반환
        return ast.parse(code).body[0].value

    return _create_ast_node


@pytest.mark.parametrize("code, expect", [
    ("print(1 + 2)", Print(expressions=["1 + 2", '3']))
])
def test_parse(create_ast_node, call_parser, code, expect):
    """
    ast.Call 타입으로 print 노드일 때 List[Print]를 생성하는지 테스트
    """
    with patch.object(CallParser, '_CallParser__print_parse',
                      return_value=Print(expressions=["1 + 2", '3'])), \
            patch.object(CallParser, "_CallParser__get_func_name", return_value='print'):
        parser = call_parser(create_ast_node(code))
        result = parser.parse()
        assert result == expect


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


@pytest.mark.parametrize("code, expect", [
    ("print(1 + 2)", Print(expressions=["1 + 2", 3])),
    ("print(a + 2)", Print(expressions=["a + 2", "1 + 2", 3]))
])
def test_print_parse(create_ast_node, call_parser, code, expect):
    """
    ast.Call 노드의 함수가 print일 때, print_parse() 함수가 제대로 동작하는지 테스트
        :param create_ast_node: 코드를 받아 ast 노드로 변환하는 함수
        :param call_parser: CallParser 인스턴스를 생성하는 함수
        :return: None
    """
    parser = call_parser(create_ast_node(code))
    result = parser._CallParser__print_parse()
    assert result == expect
