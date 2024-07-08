from app.visualize.analysis.stmt.model.assign_stmt_obj import AssignStmtObj
from app.visualize.generator.highlight.expr_highlight import ExprHighlight
from app.visualize.generator.highlight.list_highlight import ListHighlight
from app.visualize.generator.model.assign_viz import AssignViz
from app.visualize.generator.model.expr_viz import ExprViz
from app.visualize.generator.model.variable_vlz import Variable
from app.visualize.generator.visualization_manager import VisualizationManager


class AssignConverter:
    @staticmethod
    def convert(assign_obj: AssignStmtObj, viz_manager: VisualizationManager):
        assign_viz_list = []
        depth = viz_manager.get_depth()
        var_type = AssignConverter._get_var_type(assign_obj.var_type)

        highlights = AssignConverter._get_highlights(assign_obj, var_type)

        for expr_idx, expression in enumerate(assign_obj.expressions):
            expr_viz = AssignConverter._convert_to_expr_viz(
                assign_obj, depth, expr_idx, expression, highlights, var_type
            )
            assign_viz_list.append(expr_viz)

            if expr_idx == len(assign_obj.expressions) - 1:
                assign_viz = AssignConverter.convert_to_assign_viz(assign_obj, depth, expression, highlights, var_type)
                assign_viz_list.append(assign_viz)

        return assign_viz_list

    @staticmethod
    def _get_highlights(assign_obj, var_type):
        if var_type == "variable":
            return ExprHighlight.get_highlight_indexes(assign_obj.expressions)
        elif var_type in ("list", "tuple"):
            return ListHighlight.get_highlight_indexes(assign_obj.expressions)

    @staticmethod
    def _convert_to_expr_viz(assign_obj, depth, expr_idx, expression, highlights, var_type):
        return ExprViz(
            id=assign_obj.id,
            depth=depth,
            expr=expression,
            highlights=highlights[expr_idx],
            type=var_type,
        )

    @staticmethod
    def convert_to_assign_viz(assign_obj, depth, expression, highlights, var_type):
        variable_list = [
            Variable(
                depth=depth,
                expr=expression,
                highlights=highlights[-1],
                name=target,
                type=var_type,
            )
            for target in assign_obj.targets
        ]

        return AssignViz(variables=variable_list)

    @staticmethod
    def _get_var_type(var_type: str):
        if var_type in ("name", "constant", "binop"):
            var_type = "variable"

        return var_type
