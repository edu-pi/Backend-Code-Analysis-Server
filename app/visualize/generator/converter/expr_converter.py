from app.visualize.analysis.stmt.expr.model.expr_obj import PrintObj, ConstantObj, BinopObj, NameObj, RangeObj, ExprObj
from app.visualize.analysis.stmt.model.expr_stmt_obj import ExprStmtObj
from app.visualize.generator.highlight.highlight import expressions_highlight_indices
from app.visualize.generator.model.models import PrintViz, ExprViz
from app.visualize.generator.visualization_manager import VisualizationManager


class ExprConverter:

    @staticmethod
    def convert(expr_stmt_obj: ExprStmtObj, viz_manager: VisualizationManager):
        if isinstance(expr_stmt_obj.expr_obj, PrintObj):
            call_id = viz_manager.get_call_id(expr_stmt_obj)
            depth = viz_manager.get_depth()
            return ExprConverter._print_convert(expr_stmt_obj.expr_obj, call_id, depth)

        elif isinstance(expr_stmt_obj.expr_obj, ConstantObj):
            return ExprConverter._expr_convert(expr_stmt_obj.expr_obj, viz_manager.get_depth())

        elif isinstance(expr_stmt_obj.expr_obj, NameObj):
            return ExprConverter._expr_convert(expr_stmt_obj.expr_obj, viz_manager.get_depth())

        elif isinstance(expr_stmt_obj.expr_obj, BinopObj):
            return ExprConverter._expr_convert(expr_stmt_obj.expr_obj, viz_manager.get_depth())

        elif isinstance(expr_stmt_obj.expr_obj, RangeObj):
            return ExprConverter._expr_convert(expr_stmt_obj.expr_obj, viz_manager.get_depth())

        else:
            raise TypeError(f"[ExprConverter]:{type(expr_stmt_obj.expr_obj)}는 지원하지 않습니다.")

    @staticmethod
    def _print_convert(expr_obj: PrintObj, call_id, depth):

        highlights = expressions_highlight_indices(expr_obj.expressions)

        print_vizs = [
            PrintViz(
                id=call_id,
                depth=depth,
                expr=expr_obj.expressions[idx],
                highlights=highlights[idx],
                console=expr_obj.value if idx == len(expr_obj.expressions) - 1 else None,
            )
            for idx in range(len(expr_obj.expressions))
        ]

        return print_vizs

    @staticmethod
    def _expr_convert(expr_obj: ExprObj, depth):
        highlights = expressions_highlight_indices(expr_obj.expressions)

        expr_vizs = [
            ExprViz(
                value=expr_obj.value,
                type=expr_obj.type,
                expressions=expr_obj.expressions[idx],
                depth=depth,
                highlights=highlights[idx],
            )
            for idx in range(len(expr_obj.expressions))
        ]

        return expr_vizs
