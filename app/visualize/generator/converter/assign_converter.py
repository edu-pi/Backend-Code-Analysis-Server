from app.visualize.analysis.stmt.model.assign_stmt_obj import AssignStmtObj
from app.visualize.generator.highlight import highlight
from app.visualize.generator.model.models import AssignViz, Variable


class AssignConverter:
    @staticmethod
    def convert(assign_obj: AssignStmtObj):
        assign_viz_list = []
        highlights = highlight.expressions_highlight_indices(assign_obj.expressions)

        for expr_idx, expression in enumerate(assign_obj.expressions):
            variable_list = []

            for target in assign_obj.targets:
                # Todo depth 추가
                variable_list.append(Variable(name=target, expr=expression, highlights=highlights[expr_idx], depth=1))
            assign_viz_list.append(AssignViz(variables=variable_list))

        return assign_viz_list
