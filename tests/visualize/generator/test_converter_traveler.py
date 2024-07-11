import ast
from unittest.mock import MagicMock, patch

import pytest

from app.visualize.code_visualizer import CodeVisualizer
from app.visualize.generator.converter.if_converter import IfConverter
from app.visualize.generator.converter_traveler import ConverterTraveler
from app.visualize.generator.visualization_manager import VisualizationManager


@pytest.fixture
def get_if_stmt_obj():
    def _get_if_stmt_obj(code):
        code_analyzer = CodeVisualizer(ast.parse(code))
        return code_analyzer.get_analyzed_stmt_nodes()[0]

    return _get_if_stmt_obj


def test__if_convert(get_if_stmt_obj, mock_viz_manager_with_custom_depth):
    if_stmt_obj = get_if_stmt_obj("if 9 == 10:\n    print('hello')\nelif 9 < 10:\n    print('world')\n")
    with (
        patch.object(IfConverter, "get_header_define_viz") as mock_get_header_define_viz,
        patch.object(IfConverter, "get_header_change_steps") as mock_get_header_change_steps,
        patch.object(ConverterTraveler, "_get_if_body_viz_list") as mock_get_if_body_viz_list,
    ):
        mock_viz_manager = mock_viz_manager_with_custom_depth(1)
        ConverterTraveler._if_convert(if_stmt_obj, mock_viz_manager)

        # 함수들이 호출 되었는지 확인
        mock_get_header_define_viz.assert_called_once_with(if_stmt_obj.conditions, mock_viz_manager)
        mock_get_header_change_steps.assert_called_once_with(if_stmt_obj.conditions, mock_viz_manager)
        mock_get_if_body_viz_list.assert_called_once_with(if_stmt_obj.body, mock_viz_manager)


def test__get_if_body_viz_list(get_if_stmt_obj):
    if_stmt_obj = get_if_stmt_obj("if 9 == 10:\n    print('hello')\nelif 9 < 10:\n    print('world')\n")
    viz_manager = VisualizationManager()

    with patch.object(ConverterTraveler, "travel") as mock_travel:
        ConverterTraveler._get_if_body_viz_list(if_stmt_obj.body, viz_manager)

        # travel 함수가 호출 되었는지 확인
        mock_travel.assert_called_once_with(if_stmt_obj.body.body_steps, viz_manager)
