import ast
from unittest.mock import MagicMock

import pytest

from app.visualize.analysis.stmt.models.expr_stmt_obj import ExprStmtObj
from app.visualize.container.element_container import ElementContainer
from app.visualize.generator.visualization_manager import VisualizationManager


@pytest.fixture
def elem_container():
    mock = MagicMock(spec=ElementContainer)
    mock.get_element.return_value = 10
    return mock


@pytest.fixture
def set_element_return_value(elem_container):
    def _set_element_return_value(value):
        elem_container.get_element.return_value = value
        return elem_container

    return _set_element_return_value


@pytest.fixture
def viz_manager():
    viz_mockup = MagicMock(spec=VisualizationManager)
    viz_mockup.get_depth.return_value = 1

    return viz_mockup


@pytest.fixture
def mock_viz_manager_with_custom_depth():
    def _mock_viz_manager_with_custom_depth(depth):
        viz_mockup = MagicMock(spec=VisualizationManager)

        viz_mockup.increase_depth.return_value = depth + 1
        viz_mockup.get_depth.return_value = depth
        viz_mockup.decrease_depth.return_value = depth - 1

        return viz_mockup

    return _mock_viz_manager_with_custom_depth


@pytest.fixture
def create_ast():
    # 코드를 ast 노드로 변환하는 함수를 반환
    def _create_ast_node(code):
        # ast.Call 반환
        return ast.parse(code).body[0]

    return _create_ast_node


@pytest.fixture
def create_expr_stmt_obj():
    return ExprStmtObj(id=1, value="", expressions=("",), expr_type="")
