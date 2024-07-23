import pytest
from app.visualize.analysis.stmt.models.flow_control_obj import PassStmtObj, BreakStmtObj

from app.visualize.generator.converter.flow_control_converter import FlowControlConverter
from app.visualize.generator.models.flow_control_viz import FlowControlViz


@pytest.mark.parametrize(
    "flow_control_obj, expected",
    [
        pytest.param(PassStmtObj(id=1), FlowControlViz(1, 1, "pass", [0, 1, 2, 3])),
        pytest.param(BreakStmtObj(id=1), FlowControlViz(1, 1, "break", [0, 1, 2, 3, 4])),
    ],
)
def test_converter(mocker, viz_manager, flow_control_obj: PassStmtObj | BreakStmtObj, expected):
    actual = FlowControlConverter.convert(flow_control_obj, viz_manager)

    assert actual == expected
