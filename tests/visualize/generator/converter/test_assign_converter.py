import pytest

from app.visualize.analysis.stmt.model.assign_stmt_obj import AssignStmtObj
from app.visualize.generator.converter.assign_converter import AssignConverter
from app.visualize.generator.model.models import AssignViz, Variable


@pytest.fixture()
def create_assign():
    def _create_assign_obj(targets, value, expressions):
        return AssignStmtObj(targets, value, expressions)

    return _create_assign_obj


@pytest.mark.parametrize(
    "targets, value, expressions, expected",
    [
        # a = 3
        (["a"], 3, ["3"], [AssignViz([Variable(name="a", expr="3", highlights=[0], depth=1)])]),
        (  # b = a + 1
            ["b"],
            4,
            ["a + 1", "3 + 1", "4"],
            [
                AssignViz([Variable(name="b", expr="a + 1", highlights=[], depth=1)]),
                AssignViz([Variable(name="b", expr="3 + 1", highlights=[0], depth=1)]),
                AssignViz([Variable(name="b", expr="4", highlights=[0], depth=1)]),
            ],
        ),
        (  # c = d = b + 1
            ["c", "d"],
            5,
            ["b + 1", "4 + 1", "5"],
            [
                AssignViz(
                    [
                        Variable(name="c", expr="b + 1", highlights=[], depth=1),
                        Variable(name="d", expr="b + 1", highlights=[], depth=1),
                    ]
                ),
                AssignViz(
                    [
                        Variable(name="c", expr="4 + 1", highlights=[0], depth=1),
                        Variable(name="d", expr="4 + 1", highlights=[0], depth=1),
                    ]
                ),
                AssignViz(
                    [
                        Variable(name="c", expr="5", highlights=[0], depth=1),
                        Variable(name="d", expr="5", highlights=[0], depth=1),
                    ]
                ),
            ],
        ),
    ],
)
def test_convert(create_assign, targets, value, expressions, expected):
    result = AssignConverter.convert(create_assign(targets, value, expressions))

    assert result == expected
