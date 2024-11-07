from app.visualize.analysis.stmt.parser.expr.models.expr_obj import ExprObj, TupleObj
from app.visualize.utils import utils


class TupleExpr:

    @staticmethod
    def parse(elts: list[ExprObj]):
        value = TupleExpr._get_value(elts)
        expressions = TupleExpr._concat_expressions(elts)

        return TupleObj(value=value, expressions=expressions)

    @staticmethod
    def _get_value(elts: list[ExprObj]) -> tuple:
        return tuple(elt.value for elt in elts)

    @staticmethod
    def _concat_expressions(elts: list[ExprObj]):
        elts_expression_lists = [elt.expressions for elt in elts]

        # 0개의 원소를 가진 튜플인 경우
        if not elts:
            return ("()",)

        # [("a + 1", "10 + 1", "11"), ("20",)] -> [("a + 1", "20"), ("10 + 1", "20"), ("11", "20")]
        transposed_expression_lists = utils.transpose_with_last_fill(elts_expression_lists)

        # [("a + 1", "20"), ("10 + 1", "20"), ("11", "20")] -> ("[a + 1, 20]", "[10 + 1, 20]", "[11, 20]")
        return tuple(f"({', '.join(map(str, t))})" for t in transposed_expression_lists)
