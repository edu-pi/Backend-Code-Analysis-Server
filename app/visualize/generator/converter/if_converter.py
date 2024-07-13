from app.visualize.analysis.stmt.models.if_stmt_obj import (
    ConditionObj,
    IfConditionObj,
    ElifConditionObj,
    ElseConditionObj,
)
from app.visualize.generator.models.if_viz import ConditionViz, IfElseDefineViz, IfElseChangeViz
from app.visualize.generator.visualization_manager import VisualizationManager


class IfConverter:

    @staticmethod
    def get_header_define_viz(
        conditions: tuple[ConditionObj, ...], viz_manager: VisualizationManager
    ) -> IfElseDefineViz:
        if_header_conditions = []

        for condition in conditions:
            if isinstance(condition, ConditionObj):
                if_header_conditions.append(IfConverter._create_condition_viz(condition))

            else:
                raise TypeError(f"[IfConverter]: 지원하지 않는 조건문 타입입니다.: {type(condition)}")

        return IfElseDefineViz(depth=viz_manager.get_depth(), conditions=tuple(if_header_conditions))

    @staticmethod
    def get_header_change_steps(
        conditions: tuple[ConditionObj, ...], viz_manager: VisualizationManager
    ) -> list[IfElseChangeViz]:
        steps = []

        for condition in conditions:
            if not isinstance(condition, ConditionObj):
                raise TypeError(f"[IfConverter]: 지원하지 않는 조건문 타입입니다.: {type(condition)}")

            if type(condition) in (IfConditionObj, ElifConditionObj):
                for expression in condition.expressions:
                    steps.append(IfElseChangeViz(id=condition.id, depth=viz_manager.get_depth(), expr=expression))

            # 결과 처리 : condition의 결과 추가
            steps.append(IfElseChangeViz(id=condition.id, depth=viz_manager.get_depth(), expr=str(condition.result)))

            if steps[-1].expr == "True":
                return steps

        return steps

    @staticmethod
    def _create_condition_evaluation_steps(condition, viz_manager):
        # 중간 과정 생성 - 10 + 20 > 30, 30 > 30
        highlights = ExprHighlight.get_highlight_indexes(condition.expressions)

        return [
            IfElseChangeViz(
                id=condition.id,
                depth=viz_manager.get_depth(),
                expr=expression,
                highlights=highlights[idx],
            )
            for idx, expression in enumerate(condition.expressions)
        ]

    @staticmethod
    def _create_condition_result(condition, viz_manager):
        # 결과 처리 : condition의 결과 추가
        return [
            IfElseChangeViz(
                id=condition.id,
                depth=viz_manager.get_depth(),
                expr=str(condition.result),
                highlights=list(range(len(str(condition.result)))),
            )
        ]
