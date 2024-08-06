from app.visualize.analysis.stmt.models.while_stmt_obj import WhileStmtObj
from app.visualize.generator.models.while_viz import WhileDefineViz, WhileChangeConditionViz


class WhileConverter:

    @staticmethod
    def convert_to_while_define_viz(while_obj: WhileStmtObj, depth):
        return WhileDefineViz(
            id=while_obj.id,
            expr=while_obj.while_cycles[0].condition_exprs[0],
            depth=depth,
            orelse=True if while_obj.orelse else False,
        )

    @staticmethod
    def convert_to_while_change_condition_viz(call_id, while_cycle, depth):
        change_condition_steps = []

        for idx in range(len(while_cycle.condition_exprs)):
            change_condition_steps.append(
                WhileChangeConditionViz(
                    id=call_id,
                    depth=depth,
                    expr=while_cycle.condition_exprs[idx],
                )
            )

        return change_condition_steps
