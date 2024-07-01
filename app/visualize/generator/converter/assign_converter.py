from app.visualize.analysis.stmt.model.assign_stmt_obj import AssignStmtObj
from app.visualize.generator.highlight import highlight
from app.visualize.generator.model.models import AssignViz, Variable
from app.visualize.generator.visualization_manager import VisualizationManager


class AssignConverter:
    @staticmethod
    def convert(assign_obj: AssignStmtObj, viz_manager: VisualizationManager):
        assign_viz_list = []
        depth = viz_manager.get_depth()
        highlights = highlight.expressions_highlight_indices(assign_obj.expressions)

        for expr_idx, expression in enumerate(assign_obj.expressions):
            variable_list = []

            for target in assign_obj.targets:
                variable_list.append(
                    Variable(name=target, expr=expression, highlights=highlights[expr_idx], depth=depth)
                )
            assign_viz_list.append(AssignViz(variables=variable_list))

        return assign_viz_list
