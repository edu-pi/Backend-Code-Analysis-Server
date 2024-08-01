import ast

from app.visualize.analysis.stmt.models.while_stmt_obj import WhileStmtObj
from app.visualize.analysis.stmt.parser.expr.expr_traveler import ExprTraveler
from app.visualize.container.element_container import ElementContainer


class WhileStmt:

    @staticmethod
    def parse_condition(test_node: ast.expr, elem_container: ElementContainer):
        return ExprTraveler.travel(test_node, elem_container)

    @staticmethod
    def parse(call_id, while_steps, orelse_steps, orelse_id):
        return WhileStmtObj(
            id=call_id,
            while_steps=while_steps,
            orelse_steps=orelse_steps,
            orelse_id=orelse_id,
        )
