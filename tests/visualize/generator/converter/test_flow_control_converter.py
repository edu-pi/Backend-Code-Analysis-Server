from app.visualize.analysis.stmt.models.flowcontrolobj.pass_stmt_obj import PassStmtObj
from app.visualize.generator.converter.flow_control_converter import FlowControlConverter
from app.visualize.generator.models.flow_control_viz import FlowControlViz


def test_converter_pass(mock_viz_manager_with_custom_depth):
    node = PassStmtObj(id=1, expr="pass")
    actual = FlowControlConverter.convert_to_pass(node, mock_viz_manager_with_custom_depth(1))

    assert actual == FlowControlViz(id=1, depth=1, expr="pass", highlights=[0, 1, 2, 3])
