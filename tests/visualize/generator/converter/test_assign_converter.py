from unittest.mock import MagicMock

import pytest

from app.visualize.analysis.stmt.model.assign_stmt_obj import AssignStmtObj
from app.visualize.generator.converter.assign_converter import AssignConverter
from app.visualize.generator.model.models import AssignViz, Variable, ExprViz
from app.visualize.generator.visualization_manager import VisualizationManager


@pytest.fixture()
def create_assign():
    def _create_assign_obj(targets, value, expressions, var_type):
        return AssignStmtObj(id=1, targets=targets, value=value, expressions=expressions, var_type=var_type)

    return _create_assign_obj


@pytest.mark.parametrize(
    "targets, value, expressions, var_type, expected",
    [
        # a = 3
        (
            ["a"],
            3,
            ["3"],
            "constant",
            [
                ExprViz(id=1, depth=1, expr="3", highlights=[0], type="variable"),
                AssignViz(variables=[Variable(name="a", expr="3", highlights=[0], depth=1, type="variable")]),
            ],
        ),
        (  # b = a + 1
            ["b"],
            4,
            ["a + 1", "3 + 1", "4"],
            "binop",
            [
                ExprViz(id=1, depth=1, expr="a + 1", highlights=[0, 1, 2, 3, 4], type="variable"),
                ExprViz(id=1, depth=1, expr="3 + 1", highlights=[0], type="variable"),
                ExprViz(id=1, depth=1, expr="4", highlights=[0], type="variable"),
                AssignViz(variables=[Variable(name="b", expr="4", highlights=[0], depth=1, type="variable")]),
            ],
        ),
        (  # c = d = b + 1
            ["c", "d"],
            5,
            ["b + 1", "4 + 1", "5"],
            "binop",
            [
                ExprViz(id=1, depth=1, expr="b + 1", highlights=[0, 1, 2, 3, 4], type="variable"),
                ExprViz(id=1, depth=1, expr="4 + 1", highlights=[0], type="variable"),
                ExprViz(id=1, depth=1, expr="5", highlights=[0], type="variable"),
                AssignViz(
                    variables=[
                        Variable(name="c", expr="5", highlights=[0], depth=1, type="variable"),
                        Variable(name="d", expr="5", highlights=[0], depth=1, type="variable"),
                    ],
                ),
            ],
        ),
        (
            ["e"],
            [1, 2, 3],
            ["[1,2,3]"],
            "list",
            [
                ExprViz(id=1, depth=1, expr="[1,2,3]", highlights=[0, 1, 2], type="list"),
                AssignViz(
                    variables=[Variable(name="e", expr="[1,2,3]", highlights=[0, 1, 2], depth=1, type="list")],
                ),
            ],
        ),
        (
            ["f"],
            ["Hello", "World"],
            ["['Hello','World']"],
            "list",
            [
                ExprViz(id=1, depth=1, expr="['Hello','World']", highlights=[0, 1], type="list"),
                AssignViz(
                    variables=[Variable(name="f", expr="['Hello','World']", highlights=[0, 1], depth=1, type="list")],
                ),
            ],
        ),
        (
            ["g"],
            [11, "Hello"],
            ["[a + 1,b]", "[10 + 1,10]", "[11,10]"],
            "list",
            [
                ExprViz(id=1, depth=1, expr="[a + 1,b]", highlights=[0, 1], type="list"),
                ExprViz(id=1, depth=1, expr="[10 + 1,10]", highlights=[0, 1], type="list"),
                ExprViz(id=1, depth=1, expr="[11,10]", highlights=[0], type="list"),
                AssignViz(
                    variables=[Variable(name="g", expr="[11,10]", highlights=[0, 1], depth=1, type="list")],
                ),
            ],
        ),
    ],
)
def test_convert(create_assign, targets, value, expressions, var_type, expected):
    viz_manager = VisualizationManager()
    viz_manager.get_depth = MagicMock(return_value=1)

    result = AssignConverter.convert(create_assign(targets, value, expressions, var_type), viz_manager)

    assert result == expected
