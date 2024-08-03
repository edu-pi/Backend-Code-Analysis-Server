from app.visualize.analysis.stmt.models.while_stmt_obj import WhileStmtObj
from app.visualize.generator.models.while_viz import WhileDefineViz, WhileChangeConditionViz


class WhileConverter:

    @staticmethod
    def convert_to_while_define_viz(while_obj: WhileStmtObj, depth):
        return WhileDefineViz(
            id=while_obj.id,
            expr=while_obj.while_cycles[0].condition_expr[0],
            depth=depth,
        )

    @staticmethod
    def convert_to_while_change_condition_viz(call_id, while_step, depth):
        change_condition_steps = []

        for idx in range(len(while_step.condition_expr)):
            change_condition_steps.append(
                WhileChangeConditionViz(
                    id=call_id,
                    depth=depth,
                    expr=while_step.condition_expr[idx],
                )
            )

        return change_condition_steps
