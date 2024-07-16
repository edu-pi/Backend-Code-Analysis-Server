from app.visualize.analysis.stmt.models.flowcontrolobj.pass_stmt_obj import PassStmtObj
from app.visualize.generator.models.flow_control_viz import FlowControlViz
from app.visualize.generator.visualization_manager import VisualizationManager


class FlowControlConverter:

    @staticmethod
    def convert_to_pass(node: PassStmtObj, viz_manager: VisualizationManager) -> FlowControlViz:
        return FlowControlViz(
            id=node.id,
            depth=viz_manager.get_depth(),
            expr=node.expr,
            highlights=list(range(len(node.expr))),
        )

    @staticmethod
    def convert_to_continue(node: PassStmtObj, viz_manager: VisualizationManager) -> FlowControlViz:
        pass

    @staticmethod
    def convert_to_break(node: PassStmtObj, viz_manager: VisualizationManager) -> FlowControlViz:
        pass
