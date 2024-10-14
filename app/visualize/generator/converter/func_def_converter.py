from app.visualize.analysis.stmt.models.func_def_stmt_obj import FuncDefStmtObj
from app.visualize.generator.models.assign_viz import AssignViz
from app.visualize.generator.models.variable_vlz import Variable
from app.visualize.generator.visualization_manager import VisualizationManager


class FuncDefConverter:
    @staticmethod
    def convert(func_def_stmt_obj: FuncDefStmtObj, viz_manager: VisualizationManager):
        expr_stmt_obj = func_def_stmt_obj.expr_stmt_obj

        return FuncDefConverter._convert_to_assign_viz(expr_stmt_obj, func_def_stmt_obj.call_stack_name, viz_manager)

    @staticmethod
    def _convert_to_assign_viz(expr_stmt_obj, call_stack_name, viz_manager: VisualizationManager):
        return AssignViz(
            variables=[
                Variable(
                    id=expr_stmt_obj.id,
                    expr=expr_stmt_obj.expressions[0],
                    name=expr_stmt_obj.value,
                    code=viz_manager.get_code_by_idx(expr_stmt_obj.id),
                    type="function",
                )
            ],
            callStackName=call_stack_name,
        )
