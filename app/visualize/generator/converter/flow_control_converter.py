from app.visualize.analysis.stmt.models.flow_control_obj import (
    BreakStmtObj,
    PassStmtObj,
    ContinueStmtObj,
    ReturnStmtObj,
)
from app.visualize.analysis.stmt.models.stmt_type import StmtType
from app.visualize.generator.models.flow_control_viz import FlowControlViz, ReturnFlowControlViz
from app.visualize.generator.visualization_manager import VisualizationManager


class FlowControlConverter:

    @staticmethod
    def convert(node: PassStmtObj | BreakStmtObj | ContinueStmtObj | ReturnStmtObj, viz_manager: VisualizationManager):

        if node.flow_control_type is StmtType.RETURN:
            return tuple(
                ReturnFlowControlViz(
                    id=node.id,
                    depth=viz_manager.get_depth(),
                    returnExpr=expressions,
                    code=viz_manager.get_code_by_idx(node.id),
                )
                for expressions in node.expr
            )

        return (
            FlowControlViz(
                id=node.id,
                depth=viz_manager.get_depth(),
                expr=node.flow_control_type.value,
                highlights=list(range(len(node.flow_control_type.value))),
                code=viz_manager.get_code_by_idx(node.id),
            ),
        )
