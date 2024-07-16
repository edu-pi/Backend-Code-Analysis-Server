from app.visualize.analysis.stmt.models.flowcontrolobj.break_stmt_obj import BreakStmtObj
from app.visualize.analysis.stmt.models.flowcontrolobj.pass_stmt_obj import PassStmtObj
from app.visualize.generator.models.flow_control_viz import FlowControlViz
from app.visualize.generator.visualization_manager import VisualizationManager


class FlowControlConverter:

    @staticmethod
    def convert(node: PassStmtObj | BreakStmtObj, viz_manager: VisualizationManager) -> FlowControlViz:
        return FlowControlViz(
            id=node.id,
            depth=viz_manager.get_depth(),
            expr=node.expr,
            highlights=list(range(len(node.expr))),
        )
