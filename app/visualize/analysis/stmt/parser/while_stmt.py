import ast

from app.visualize.analysis.stmt.models.while_stmt_obj import WhileStmtObj
from app.visualize.analysis.stmt.parser.expr.expr_traveler import ExprTraveler
from app.visualize.analysis.stmt.parser.expr.models.expr_obj import ExprObj
from app.visualize.container.element_container import ElementContainer


class WhileStmt:

    @staticmethod
    def parse_condition(test_node: ast.expr, elem_container: ElementContainer):
        test_obj = ExprTraveler.travel(test_node, elem_container)
        return WhileStmt.add_bool_if_not_Condition(test_obj)

    @staticmethod
    def parse(call_id, while_steps, orelse_steps, orelse_id):
        return WhileStmtObj(
            id=call_id,
            while_steps=while_steps,
            orelse_steps=orelse_steps,
            orelse_id=orelse_id,
        )

    @staticmethod
    def add_bool_if_not_Condition(test_obj: ExprObj):
        if test_obj.expressions[-1] in ("True", "False"):
            return test_obj

        condition = "True" if test_obj.value else "False"

        return ExprObj(value=test_obj.value, expressions=test_obj.expressions[:] + (condition,), type=test_obj.type)
