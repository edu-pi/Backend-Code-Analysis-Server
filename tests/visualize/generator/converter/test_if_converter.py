import pytest

from app.visualize.analysis.stmt.models.if_stmt_obj import (
    IfConditionObj,
    ElifConditionObj,
    ElseConditionObj,
    ConditionObj,
)
from app.visualize.generator.converter.if_converter import IfConverter
from app.visualize.generator.models.if_viz import ConditionViz, IfElseChangeViz
from app.visualize.generator.visualization_manager import VisualizationManager


@pytest.mark.parametrize(
    "conditions, expected",
    [
        (
            (
                IfConditionObj(
                    id=1,
                    expressions=(
                        "a > b",
                        "12 > 10",
                    ),
                    result=True,
                ),
                ElifConditionObj(
                    id=2,
                    expressions=(
                        "a < b",
                        "12 < 10",
                    ),
                    result=False,
                ),
                ElseConditionObj(
                    id=3,
                    expressions=None,
                    result=False,
                ),
            ),
            (
                ConditionViz(id=1, expr="a > b", type="if"),
                ConditionViz(id=2, expr="a < b", type="elif"),
                ConditionViz(id=3, expr="", type="else"),
            ),
        )
    ],
)
def test_get_header_define_viz(conditions: tuple[ConditionObj, ...], expected):
    actual = IfConverter.get_header_define_viz(conditions, VisualizationManager())
    assert actual.conditions == expected


@pytest.mark.parametrize(
    "conditions,expected",
    [
        pytest.param(
            (IfConditionObj(id=1, expressions=("a > b", "10 > 20"), result=False),),
            [
                IfElseChangeViz(id=1, depth=1, expr="a > b"),
                IfElseChangeViz(id=1, depth=1, expr="10 > 20"),
                IfElseChangeViz(id=1, depth=1, expr="False"),
            ],
            id="if문 False인 경우",
        ),
        pytest.param(
            (ElseConditionObj(id=1, expressions=None, result=True),),
            [
                IfElseChangeViz(id=1, depth=1, expr="True"),
            ],
            id="else문 True인 경우",
        ),
    ],
)
def test_get_header_change_steps(conditions: tuple[ConditionObj, ...], expected, mock_viz_manager_with_custom_depth):
    assert IfConverter.get_header_change_steps(conditions, mock_viz_manager_with_custom_depth(1)) == expected


@pytest.mark.parametrize(
    "condition, condition_type, expected",
    [
        pytest.param(
            IfConditionObj(
                id=1,
                expressions=(
                    "a > b",
                    "12 > 10",
                ),
                result=True,
            ),
            "if",
            ConditionViz(id=1, expr="a > b", type="if"),
            id="if문 Condition viz 생성",
        ),
        pytest.param(
            ElifConditionObj(
                id=1,
                expressions=(
                    "a < b",
                    "12 < 10",
                ),
                result=False,
            ),
            "elif",
            ConditionViz(id=1, expr="a < b", type="elif"),
            id="elif문 Condition viz 생성",
        ),
        pytest.param(
            ElseConditionObj(
                id=1,
                expressions=None,
                result=False,
            ),
            "else",
            ConditionViz(id=1, expr="", type="else"),
            id="else Condition viz 생성",
        ),
    ],
)
def test__create_condition_viz(condition: ConditionObj, condition_type, expected):
    assert IfConverter._create_condition_viz(condition) == expected
