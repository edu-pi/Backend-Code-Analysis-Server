from app.visualize.analysis.element_manager import CodeElementManager
from app.visualize.analysis.stmt.expr.model.expr_obj import ExprObj
from app.visualize.analysis.stmt.model.expr_stmt_obj import ExprStmtObj
from app.visualize.generator.highlight.highlight import expressions_highlight_indices
from app.visualize.generator.model.models import PrintViz


class ExprConverter:

    @staticmethod
    def convert(expr_stmt_obj: ExprStmtObj, elem_manager: CodeElementManager):
        if expr_stmt_obj.expr_obj.type == "print":
            call_id = elem_manager.get_call_id(expr_stmt_obj)
            depth = elem_manager.get_depth
            return ExprConverter.print_convert(expr_stmt_obj.expr_obj, call_id, depth)

    @staticmethod
    def print_convert(expr_obj: ExprObj, call_id, depth):

        highlights = expressions_highlight_indices(expr_obj.expressions)

        print_vizs = [
            PrintViz(
                id=call_id,
                depth=depth,
                expr=expr_obj.expressions[idx],
                highlight=highlights[idx],
                console=expr_obj.value if idx == len(expr_obj.expressions) - 1 else None,
            )
            for idx in range(len(expr_obj.expressions))
        ]

        return print_vizs
