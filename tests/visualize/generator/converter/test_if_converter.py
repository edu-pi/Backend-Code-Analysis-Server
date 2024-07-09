import pytest

from app.visualize.analysis.stmt.model.if_stmt_obj import (
    IfConditionObj,
    ElifConditionObj,
    ConditionObj,
    ElseConditionObj,
)
from app.visualize.generator.converter.if_converter import IfConverter
from app.visualize.generator.model.if_viz import ConditionViz


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
