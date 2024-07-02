from unittest.mock import patch, MagicMock

import pytest

from app.visualize.analysis.stmt.model.assign_stmt_obj import AssignStmtObj
from app.visualize.generator.converter.assign_converter import AssignConverter
from app.visualize.generator.model.models import AssignViz, Variable
from app.visualize.generator.visualization_manager import VisualizationManager


@pytest.fixture()
def create_assign():
    def _create_assign_obj(targets, value, expressions):
        return AssignStmtObj(id=1, targets=targets, value=value, expressions=expressions)

    return _create_assign_obj


@pytest.mark.parametrize(
    "targets, value, expressions, expected",
    [
        # a = 3
        (["a"], 3, ["3"], [AssignViz(id=1, variables=[Variable(name="a", expr="3", highlights=[0], depth=1)])]),
        (  # b = a + 1
            ["b"],
            4,
            ["a + 1", "3 + 1", "4"],
            [
                AssignViz(id=1, variables=[Variable(name="b", expr="a + 1", highlights=[0, 1, 2, 3, 4], depth=1)]),
                AssignViz(id=1, variables=[Variable(name="b", expr="3 + 1", highlights=[0], depth=1)]),
                AssignViz(id=1, variables=[Variable(name="b", expr="4", highlights=[0], depth=1)]),
            ],
        ),
        (  # c = d = b + 1
            ["c", "d"],
            5,
            ["b + 1", "4 + 1", "5"],
            [
                AssignViz(
                    id=1,
                    variables=[
                        Variable(name="c", expr="b + 1", highlights=[0, 1, 2, 3, 4], depth=1),
                        Variable(name="d", expr="b + 1", highlights=[0, 1, 2, 3, 4], depth=1),
                    ],
                ),
                AssignViz(
                    id=1,
                    variables=[
                        Variable(name="c", expr="4 + 1", highlights=[0], depth=1),
                        Variable(name="d", expr="4 + 1", highlights=[0], depth=1),
                    ],
                ),
                AssignViz(
                    id=1,
                    variables=[
                        Variable(name="c", expr="5", highlights=[0], depth=1),
                        Variable(name="d", expr="5", highlights=[0], depth=1),
                    ],
                ),
            ],
        ),
    ],
)
def test_convert(create_assign, targets, value, expressions, expected):
    viz_manager = VisualizationManager()
    viz_manager.get_depth = MagicMock(return_value=1)

    result = AssignConverter.convert(create_assign(targets, value, expressions), viz_manager)

    assert result == expected
