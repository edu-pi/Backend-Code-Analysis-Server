# for_stmt_obj를 받아서 for_viz를 반환하는 클래스
from app.visualize.analysis.stmt.expr.model.range_expr_obj import RangeExprObj
from app.visualize.analysis.stmt.model.for_stmt_obj import ForStmtObj


class ForConvertor:

    @staticmethod
    def convert(for_stmt: ForStmtObj):
        # condition
        iter_obj = for_stmt.iter_obj
        start, end, step = ForConvertor._get_condition(iter_obj)
        # header
        for i in range(start, end, step):
            pass
            # header

            # body
        # body


    @staticmethod
    def _get_condition(iter_obj: RangeExprObj):
        if isinstance(iter_obj, RangeExprObj):
            return iter_obj.expressions[-1]

        else:
            raise ValueError("Invalid iter_obj type")

    @staticmethod
    def _get_header(target_name:str, iter_obj: RangeExprObj):
        pass
