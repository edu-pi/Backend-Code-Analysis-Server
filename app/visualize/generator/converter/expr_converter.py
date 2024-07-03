from app.visualize.analysis.stmt.expr.model.expr_obj import PrintObj, ConstantObj, BinopObj, NameObj, RangeObj, ExprObj
from app.visualize.analysis.stmt.model.expr_stmt_obj import ExprStmtObj
from app.visualize.generator.highlight.expr_highlight import ExprHighlight
from app.visualize.generator.model.models import PrintViz, ExprViz
from app.visualize.generator.visualization_manager import VisualizationManager


class ExprConverter:

    @staticmethod
    def convert(expr_stmt_obj: ExprStmtObj, viz_manager: VisualizationManager):
        call_id = expr_stmt_obj.id
        depth = viz_manager.get_depth()

        if isinstance(expr_stmt_obj.expr_obj, PrintObj):
            return ExprConverter._print_convert(expr_stmt_obj.expr_obj, call_id, depth)

        elif isinstance(expr_stmt_obj.expr_obj, ConstantObj):
            return ExprConverter._expr_convert(expr_stmt_obj.expr_obj, call_id, depth)

        elif isinstance(expr_stmt_obj.expr_obj, NameObj):
            return ExprConverter._expr_convert(expr_stmt_obj.expr_obj, call_id, depth)

        elif isinstance(expr_stmt_obj.expr_obj, BinopObj):
            return ExprConverter._expr_convert(expr_stmt_obj.expr_obj, call_id, depth)

        else:
            raise TypeError(f"[ExprConverter]:{type(expr_stmt_obj.expr_obj)}는 지원하지 않습니다.")

    @staticmethod
    def _print_convert(expr_obj: PrintObj, call_id, depth):
        highlights = ExprHighlight.get_highlight_attr(expr_obj.expressions)

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
    def _expr_convert(expr_obj: ExprObj, call_id, depth):
        highlights = ExprHighlight.get_highlight_attr(expr_obj.expressions)

        expr_vizs = [
            ExprViz(
                id=call_id,
                depth=depth,
                expr=expr_obj.expressions[idx],
                highlights=highlights[idx],
                type=expr_obj.type,
            )
            for idx in range(len(expr_obj.expressions))
        ]

        return expr_vizs
