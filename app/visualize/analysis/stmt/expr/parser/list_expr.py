import ast

from app.visualize.analysis.stmt.expr.expr_util import util
from app.visualize.analysis.stmt.expr.model.expr_obj import ListObj


class ListExpr:

    @staticmethod
    def parse(elts):
        value = ListExpr._get_value(elts)
        expressions = ListExpr._concat_expression(elts)

        return ListObj(value=value, expressions=expressions)

    @staticmethod
    def _get_value(elts):
        return tuple(elt.value for elt in elts)

    @staticmethod
    def _concat_expression(elts):
        elts_lists = [elt.expressions for elt in elts]
        transposed_lists = util.transpose_with_last_fill(elts_lists)

        return tuple(f"[{','.join(map(str, t))}]" for t in transposed_lists)
