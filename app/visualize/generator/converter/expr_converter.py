from app.visualize.analysis.stmt.expr.model.expr_obj import PrintObj, ConstantObj, BinopObj, NameObj, RangeObj, ExprObj
from app.visualize.analysis.stmt.model.expr_stmt_obj import ExprStmtObj
from app.visualize.generator.highlight.expr_highlight import ExprHighlight
from app.visualize.generator.model.expr_viz import ExprViz
from app.visualize.generator.model.print_viz import PrintViz
from app.visualize.generator.highlight.list_highlight import ListHighlight
from app.visualize.generator.visualization_manager import VisualizationManager


class ExprConverter:

    @staticmethod
    def convert(expr_stmt_obj: ExprStmtObj, viz_manager: VisualizationManager):
        call_id = expr_stmt_obj.id
        depth = viz_manager.get_depth()
        var_type = ExprConverter._get_var_type(expr_stmt_obj.var_type)

        if var_type == "variable":
            return ExprConverter._convert_to_expr_viz(expr_stmt_obj, var_type, call_id, depth)

        elif var_type == "list":
            return ExprConverter._convert_to_expr_viz(expr_stmt_obj, var_type, call_id, depth)

        elif var_type == "print":
            return ExprConverter._convert_to_print_viz(expr_stmt_obj, call_id, depth)

        else:
            raise TypeError(f"[ExprConverter]:{var_type}는 지원하지 않습니다.")

    @staticmethod
    def _get_var_type(var_type: str):
        if var_type in ("name", "constant", "binop"):
            var_type = "variable"

        return var_type

    @staticmethod
    def _convert_to_expr_viz(expr_stmt_obj: ExprStmtObj, var_type, call_id, depth):
        highlights = ExprHighlight.get_highlight_indexes(expr_stmt_obj.expressions)
        if var_type == "list":
            highlights = ListHighlight.get_highlight_indexes(expr_stmt_obj.expressions)

        expr_vizs = [
            ExprViz(
                id=call_id,
                depth=depth,
                expr=expr_stmt_obj.expressions[idx],
                highlights=highlights[idx],
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
