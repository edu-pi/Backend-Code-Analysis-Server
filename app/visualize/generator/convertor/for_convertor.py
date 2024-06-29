# for_stmt_obj를 받아서 for_viz를 반환하는 클래스
from app.visualize.analysis.stmt.expr.model.range_expr_obj import RangeExprObj
from app.visualize.analysis.stmt.model.for_stmt_obj import ForStmtObj
from app.visualize.generator.model.models import ConditionViz, ForViz
from app.visualize.generator.visualization_manager import VisualizationManager


class ForConvertor:

    @staticmethod
    def convert(for_stmt: ForStmtObj, viz_manager: VisualizationManager):
        # condition
        target_name = for_stmt.target_name
        iter_obj = for_stmt.iter_obj
        # header
        for i in for_stmt.iter_obj.iterator:
            # header
            header_viz = ForConvertor._get_header(for_stmt.target_name, iter_obj, viz_manager)
        # body
        return header_viz

    @staticmethod
    def _get_condition(target_name: str, iter_obj: RangeExprObj):
        if isinstance(iter_obj, RangeExprObj):
            return ForConvertor._get_range_condition(target_name, iter_obj)

        else:
            raise ValueError("Invalid iter_obj type")

    @staticmethod
    def _get_header(target_name: str, iter_obj: RangeExprObj, viz_manager: VisualizationManager):
        call_id = viz_manager.get_call_id(iter_obj)
        depth = viz_manager.get_depth()
        condition = ForConvertor._get_condition(target_name, iter_obj)
        # highlight

        highlight = []
        return ForViz(id=call_id, depth=depth, condition=condition, highlight=highlight)

    @staticmethod
    def _get_range_condition(target_name, iter_obj):
        condition_value = iter_obj.expressions[-1]

        return ConditionViz(
            target_name,
            cur=condition_value.start,
            start=condition_value.start,
            end=condition_value.end,
            step=condition_value.step,
        )
