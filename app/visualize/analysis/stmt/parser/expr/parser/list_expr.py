from app.visualize.analysis.stmt.parser.expr.models.expr_obj import ListObj, ExprObj
from app.visualize.utils import utils


class ListExpr:

    @staticmethod
    def parse(elts: list[ExprObj]):
        value = ListExpr._get_value(elts)
        expressions = ListExpr._concat_expression(elts)

        return ListObj(value=value, expressions=expressions)

    @staticmethod
    def _get_value(elts: list[ExprObj]):
        return [elt.value for elt in elts]

    @staticmethod
    def _concat_expression(elts: list[ExprObj]):
        elts_expression_lists = [elt.expressions for elt in elts]

        # [("a + 1", "10 + 1", "11"), ("20",)] -> [("a + 1", "20"), ("10 + 1", "20"), ("11", "20")]
        transposed_expression_lists = utils.transpose_with_last_fill(elts_expression_lists)

        # [("a + 1", "20"), ("10 + 1", "20"), ("11", "20")] -> ("[a + 1,20]", "[10 + 1,20]", "[11,20]")
        return tuple(f"[{','.join(map(str, t))}]" for t in transposed_expression_lists)
