import ast

from app.visualize.container.element_container import ElementContainer
from app.visualize.analysis.stmt.parser.expr.expr_traveler import ExprTraveler
from app.visualize.analysis.stmt.models.if_stmt_obj import ElseConditionObj, IfConditionObj, ElifConditionObj


class IfStmt:

    @staticmethod
    def parse_if_condition(test_node: ast.expr, elem_container: ElementContainer):
        test_obj = ExprTraveler.travel(test_node, elem_container)

        return IfConditionObj(
            id=test_node.lineno,
            expressions=test_obj.expressions,
            result=test_obj.value,
        )

    @staticmethod
    def parse_elif_condition(test_node: ast.expr, elem_container: ElementContainer):
        test_obj = ExprTraveler.travel(test_node, elem_container)

        return ElifConditionObj(
            id=test_node.lineno,
            expressions=test_obj.expressions,
            result=test_obj.value,
        )

    @staticmethod
    def parse_else_condition(else_body_node: ast.stmt, result: bool):
        return ElseConditionObj(id=else_body_node.lineno - 1, expressions=None, result=result)
