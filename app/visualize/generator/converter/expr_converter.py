from app.visualize.analysis.stmt.models.expr_stmt_obj import ExprStmtObj
from app.visualize.generator.highlight.expr_highlight import ExprHighlight
from app.visualize.generator.models.append_viz import AppendViz
from app.visualize.generator.models.expr_viz import ExprViz
from app.visualize.generator.models.print_viz import PrintViz
from app.visualize.generator.models.variable_vlz import Variable
from app.visualize.generator.visualization_manager import VisualizationManager
from app.visualize.utils import utils


class ExprConverter:

    @staticmethod
    def convert(expr_stmt_obj: ExprStmtObj, viz_manager: VisualizationManager):
        call_id = expr_stmt_obj.id
        depth = viz_manager.get_depth()
        var_type = utils.get_var_type(expr_stmt_obj.value, expr_stmt_obj.expr_type)

        if var_type == "variable":
            return ExprConverter._convert_to_expr_viz(expr_stmt_obj, var_type, call_id, depth)

        elif var_type == "list":
            return ExprConverter._convert_to_expr_viz(expr_stmt_obj, var_type, call_id, depth)

        elif var_type == "print":
            return ExprConverter._convert_to_print_viz(expr_stmt_obj, call_id, depth)

        elif var_type == "append":
            return ExprConverter._convert_to_append_viz(expr_stmt_obj, call_id, depth)

        else:
            raise TypeError(f"[ExprConverter]:{var_type}는 지원하지 않습니다.")

    @staticmethod
    def _convert_to_expr_viz(expr_stmt_obj: ExprStmtObj, var_type, call_id, depth):
        expr_vizs = [
            ExprViz(
                id=call_id,
                depth=depth,
                expr=expr_stmt_obj.expressions[idx],
                type=var_type,
            )
            for idx in range(len(expr_stmt_obj.expressions))
        ]

        return expr_vizs

    @staticmethod
    def _convert_to_print_viz(expr_stmt_obj: ExprStmtObj, call_id, depth):
        highlights = ExprHighlight.get_highlight_indexes(expr_stmt_obj.expressions)

        print_vizs = [
            PrintViz(
                id=call_id,
                depth=depth,
                expr=expr_stmt_obj.expressions[idx],
                highlights=highlights[idx],
                console=expr_stmt_obj.value if idx == len(expr_stmt_obj.expressions) - 1 else None,
            )
            for idx in range(len(expr_stmt_obj.expressions))
        ]

        return print_vizs

    @staticmethod
    def _convert_to_append_viz(expr_stmt_obj: ExprStmtObj, call_id, depth):
        append_vizs = []
        var_type = utils.check_list(expr_stmt_obj.expressions[-1])
        expr_vizs = ExprConverter._convert_to_expr_viz(expr_stmt_obj, var_type, call_id, depth)
        append_vizs.extend(expr_vizs)

        append_vizs.append(
            AppendViz(
                variable=Variable(
                    id=call_id,
                    expr=expr_stmt_obj.expressions[-1],
                    name=expr_stmt_obj.value,
                    type=var_type,
                ),
            )
        )

        return append_vizs
