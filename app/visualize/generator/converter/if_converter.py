from app.visualize.analysis.stmt.models.if_stmt_obj import (
    ConditionObj,
)
from app.visualize.generator.models.if_viz import ConditionViz, IfElseDefineViz, IfElseChangeViz
from app.visualize.generator.visualization_manager import VisualizationManager


class IfConverter:

    @staticmethod
    def convert_to_if_else_define_viz(
        conditions: tuple[ConditionObj, ...], viz_manager: VisualizationManager
    ) -> IfElseDefineViz:
        if_header_conditions = []

        for condition in conditions:
            if not isinstance(condition, ConditionObj):
                raise TypeError(f"[IfConverter]: 지원하지 않는 조건문 타입입니다.: {type(condition)}")

            if_header_conditions.append(IfConverter._create__if_else_define_viz(condition, viz_manager))

        return IfElseDefineViz(depth=viz_manager.get_depth(), conditions=tuple(if_header_conditions))

    @staticmethod
    def _create__if_else_define_viz(condition: ConditionObj, viz_manager: VisualizationManager) -> ConditionViz:
        expr = condition.expressions[0] if condition.type != "else" else ""
        return ConditionViz(
            id=condition.id, expr=expr, type=condition.type.value, code=viz_manager.get_code_by_idx(condition.id)
        )

    @staticmethod
    def convert_to_if_else_change_viz(
        conditions: tuple[ConditionObj, ...], viz_manager: VisualizationManager
    ) -> list[IfElseChangeViz]:
        steps = []

        for condition in conditions:
            if not isinstance(condition, ConditionObj):
                raise TypeError(f"[IfConverter]: 지원하지 않는 조건문 타입입니다.: {type(condition)}")

            # 조건식 평가 과정 추가
            steps.extend(IfConverter._create_condition_evaluation_steps(condition, viz_manager))

            if condition.result:
                break

        return steps

    @staticmethod
    def _create_condition_evaluation_steps(
        condition: ConditionObj, viz_manager: VisualizationManager
    ) -> list[IfElseChangeViz]:
        # 중간 과정 생성 - 10 + 20 > 30, 30 > 30

        return [
            IfElseChangeViz(
                id=condition.id,
                depth=viz_manager.get_depth(),
                expr=expression,
            )
            for idx, expression in enumerate(condition.expressions)
        ]

    @staticmethod
    def _create_condition_result(condition: ConditionObj, viz_manager: VisualizationManager) -> list[IfElseChangeViz]:
        # 결과 처리 : condition의 결과 추가
        return [
            IfElseChangeViz(
                id=condition.id,
                depth=viz_manager.get_depth(),
                expr=str(condition.result),
            )
        ]
