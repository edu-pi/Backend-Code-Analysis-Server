from unittest.mock import MagicMock

import pytest

from app.visualize.analysis.stmt.model.assign_stmt_obj import AssignStmtObj
from app.visualize.analysis.stmt.model.expr_stmt_obj import ExprStmtObj
from app.visualize.generator.converter.assign_converter import AssignConverter
from app.visualize.generator.model.assign_viz import AssignViz
from app.visualize.generator.model.variable_vlz import Variable
from app.visualize.generator.visualization_manager import VisualizationManager


@pytest.fixture()
def create_assign():
    def _create_assign_obj(targets, value, expressions, var_type):
        return AssignStmtObj(
            targets=targets, expr_stmt_obj=ExprStmtObj(id=1, value=value, expressions=expressions, var_type=var_type)
        )

    return _create_assign_obj


@pytest.mark.parametrize(
    "targets, value, expressions, var_type, expected",
    [
        pytest.param(
            ["a"],
            3,
            ["3"],
            "constant",
            AssignViz(variables=[Variable(id=1, name="a", expr="3", highlights=[0], depth=1, type="variable")]),
            id="a = 3: success case",
        ),
        pytest.param(
            ["b"],
            4,
            ["a + 1", "3 + 1", "4"],
            "binop",
            AssignViz(variables=[Variable(id=1, name="b", expr="4", highlights=[0], depth=1, type="variable")]),
            id="b = a + 1: success case",
        ),
        pytest.param(
            ["c", "d"],
            5,
            ["b + 1", "4 + 1", "5"],
            "binop",
            AssignViz(
                variables=[
                    Variable(id=1, name="c", expr="5", highlights=[0], depth=1, type="variable"),
                    Variable(id=1, name="d", expr="5", highlights=[0], depth=1, type="variable"),
                ],
            ),
            id="c, d = b + 1: success case",
        ),
        pytest.param(
            ["e"],
            [1, 2, 3],
            ["[1,2,3]"],
            "list",
            AssignViz(
                variables=[Variable(id=1, name="e", expr="[1,2,3]", highlights=[0, 1, 2], depth=1, type="list")],
            ),
            id="e = [1, 2, 3]: success case",
        ),
        pytest.param(
            ["f"],
            ["Hello", "World"],
            ["['Hello','World']"],
            "list",
            AssignViz(
                variables=[Variable(id=1, name="f", expr="['Hello','World']", highlights=[0, 1], depth=1, type="list")],
            ),
            id="f = ['Hello', 'World']: success case",
        ),
        pytest.param(
            ["g"],
            [11, "Hello"],
            ["[a + 1,b]", "[10 + 1,10]", "[11,10]"],
            "list",
            AssignViz(
                variables=[Variable(id=1, name="g", expr="[11,10]", highlights=[0, 1], depth=1, type="list")],
            ),
            id="g = [a + 1, b]: success case",
        ),
    ],
)
def test_convert(create_assign, targets, value, expressions, var_type, expected):
    viz_manager = VisualizationManager()
    viz_manager.get_depth = MagicMock(return_value=1)

    result = AssignConverter.convert(create_assign(targets, value, expressions, var_type), viz_manager)

    assert result == expected
