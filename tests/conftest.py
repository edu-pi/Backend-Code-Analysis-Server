import ast
from unittest.mock import MagicMock

import pytest

from app.visualize.analysis.element_manager import CodeElementManager


@pytest.fixture
def elem_manager():
    mock = MagicMock(spec=CodeElementManager)
    mock.get_element.return_value = 10
    return mock


@pytest.fixture
def create_ast():
    # 코드를 ast 노드로 변환하는 함수를 반환
    def _create_ast_node(code):
        # ast.Call 반환
        return ast.parse(code).body[0]

    return _create_ast_node
