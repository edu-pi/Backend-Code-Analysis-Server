# for_stmt_obj를 받아서 for_viz를 반환하는 클래스
from app.visualize.analysis.stmt.expr.models.expr_obj import RangeObj
from app.visualize.analysis.stmt.models.for_stmt_obj import ForStmtObj
from app.visualize.generator.highlight.for_highlight import ForHighlight
from app.visualize.generator.model.for_viz import ForViz, ForConditionViz
from app.visualize.generator.visualization_manager import VisualizationManager


class ForHeaderConvertor:

    @staticmethod
    def convert(for_stmt: ForStmtObj, viz_manager: VisualizationManager):
        # condition
        call_id = for_stmt.id
        target_name = for_stmt.target_name
        iter_obj = for_stmt.iter_obj

        return ForHeaderConvertor._header_convert(call_id, target_name, iter_obj, viz_manager)

    @staticmethod
    def get_updated_header(header_viz: ForViz, new_cur):
        new_condition = header_viz.condition.copy_with_cur(new_cur)

        return header_viz.update(new_condition, ForHighlight.get_highlight_attr(new_condition))

    @staticmethod
    def _header_convert(call_id: int, target_name: str, iter_obj: RangeObj, viz_manager: VisualizationManager):
        depth = viz_manager.get_depth()
        condition = ForHeaderConvertor._get_condition(target_name, iter_obj)
        highlight = ForHighlight.get_highlight_attr(condition)

        return ForViz(id=call_id, depth=depth, condition=condition, highlights=highlight)

    @staticmethod
    def _get_condition(target_name: str, iter_obj: RangeObj):
        if isinstance(iter_obj, RangeObj):
            return ForHeaderConvertor._get_range_condition(target_name, iter_obj)

        else:
            raise ValueError("Invalid iter_obj type")

    @staticmethod
    def _get_range_condition(target_name, iter_obj):
        condition_value = iter_obj.expressions[-1]

        return ForConditionViz(
            target_name,
            cur=condition_value.start,
            start=condition_value.start,
            end=condition_value.end,
            step=condition_value.step,
        )
