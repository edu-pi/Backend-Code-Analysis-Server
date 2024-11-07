from app.visualize.analysis.stmt.models.return_stmt_obj import ReturnStmtObj
from app.visualize.generator.models.flow_control_viz import ReturnFlowControlViz
from app.visualize.generator.visualization_manager import VisualizationManager


class ReturnConverter:
    @staticmethod
    def convert(node: ReturnStmtObj, viz_manager: VisualizationManager):
        return tuple(
            ReturnFlowControlViz(
                id=node.id,
                depth=viz_manager.get_depth(),
                returnExpr=expressions,
                code=viz_manager.get_code_by_idx(node.id),
            )
            for expressions in node.expr
        )
