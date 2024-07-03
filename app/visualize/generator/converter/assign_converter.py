from app.visualize.analysis.stmt.model.assign_stmt_obj import AssignStmtObj
from app.visualize.generator.highlight import highlight
from app.visualize.generator.model.models import AssignViz, Variable, ExprViz
from app.visualize.generator.visualization_manager import VisualizationManager


class AssignConverter:
    @staticmethod
    def convert(assign_obj: AssignStmtObj, viz_manager: VisualizationManager):
        assign_viz_list = []
        depth = viz_manager.get_depth()
        highlights = highlight.expressions_highlight_indices(assign_obj.expressions)

        for expr_idx, expression in enumerate(assign_obj.expressions):
            expr_viz = AssignConverter.assign_expr_convert(assign_obj, depth, expr_idx, expression, highlights)
            assign_viz_list.append(expr_viz)

            if expr_idx == len(assign_obj.expressions) - 1:
                assign_viz = AssignConverter.assign_viz_convert(assign_obj, depth, expr_idx, expression, highlights)
                assign_viz_list.append(assign_viz)

        return assign_viz_list

    @staticmethod
    def assign_expr_convert(assign_obj, depth, expr_idx, expression, highlights):
        return ExprViz(
            id=assign_obj.id,
            depth=depth,
            expr=expression,
            highlights=highlights[expr_idx],
            type=AssignConverter._get_var_type(assign_obj.var_type),
        )

    @staticmethod
    def assign_viz_convert(assign_obj, depth, expr_idx, expression, highlights):
        variable_list = [
            Variable(
                depth=depth,
                expr=expression,
                highlights=highlights[expr_idx],
                name=target,
                type=AssignConverter._get_var_type(assign_obj.var_type),
            )
            for target in assign_obj.targets
        ]

        return AssignViz(variables=variable_list)

    @staticmethod
    def _get_var_type(var_type: str):
        if var_type in ("name", "constant", "binop"):
            var_type = "variable"

        return var_type
