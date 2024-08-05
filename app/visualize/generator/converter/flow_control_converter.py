from app.visualize.analysis.stmt.models.flow_control_obj import BreakStmtObj, PassStmtObj, ContinueStmtObj
from app.visualize.generator.models.flow_control_viz import FlowControlViz
from app.visualize.generator.visualization_manager import VisualizationManager


class FlowControlConverter:

    @staticmethod
    def convert(
        node: PassStmtObj | BreakStmtObj | ContinueStmtObj, viz_manager: VisualizationManager
    ) -> FlowControlViz:
        return FlowControlViz(
            id=node.id,
            depth=viz_manager.get_depth(),
            expr=node.flow_control_type.value,
            highlights=list(range(len(node.flow_control_type.value))),
            code=viz_manager.get_code_by_idx(node.id),
        )
