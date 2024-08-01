from app.visualize.analysis.stmt.models.while_stmt_obj import WhileStmtObj
from app.visualize.generator.highlight.expr_highlight import ExprHighlight
from app.visualize.generator.models.while_viz import WhileDefineViz, WhileChangeConditionViz


class WhileConverter:

    @staticmethod
    def convert_to_while_define_viz(while_obj: WhileStmtObj, depth):
        return WhileDefineViz(
            id=while_obj.id,
            expr=while_obj.while_steps[0].condition_expr[0],
            depth=depth,
            orelse=True if len(while_obj.orelse_steps) > 0 else False,
            orelseId=while_obj.orelse_id,
        )

    @staticmethod
    def convert_to_while_change_condition_viz(call_id, while_step, depth):
        change_condition_steps = []
        highlights = ExprHighlight.get_highlight_indexes(while_step.condition_expr)

        for idx in range(len(while_step.condition_expr)):
            change_condition_steps.append(
                WhileChangeConditionViz(
                    id=call_id,
                    depth=depth,
                    expr=while_step.condition_expr[idx],
                    highlights=highlights[idx],
                )
            )

        return change_condition_steps
