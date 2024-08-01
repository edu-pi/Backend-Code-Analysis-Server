import ast

from app.visualize.analysis.stmt.models.if_stmt_obj import ElseConditionObj, IfConditionObj, ElifConditionObj
from app.visualize.analysis.stmt.parser.expr.expr_traveler import ExprTraveler
from app.visualize.analysis.stmt.parser.expr.models.expr_obj import ExprObj
from app.visualize.container.element_container import ElementContainer


class IfStmt:

    @staticmethod
    def parse_if_condition(test_node: ast.expr, elem_container: ElementContainer):
        test_obj = ExprTraveler.travel(test_node, elem_container)
        test_obj_with_bool = IfStmt.add_bool_if_not_Condition(test_obj)

        return IfConditionObj(
            id=test_node.lineno,
            expressions=test_obj_with_bool.expressions,
            result=test_obj_with_bool.value,
        )

    @staticmethod
    def parse_elif_condition(test_node: ast.expr, elem_container: ElementContainer):
        test_obj = ExprTraveler.travel(test_node, elem_container)
        test_obj = IfStmt.add_bool_if_not_Condition(test_obj)

        return ElifConditionObj(
            id=test_node.lineno,
            expressions=test_obj.expressions,
            result=test_obj.value,
        )

    @staticmethod
    def parse_else_condition(else_body_node: ast.stmt, result: bool):
        return ElseConditionObj(id=else_body_node.lineno - 1, expressions=None, result=result)

    @staticmethod
    def add_bool_if_not_Condition(test_obj: ExprObj):
        if test_obj.expressions[-1] in ("True", "False"):
            return test_obj

        condition = "True" if test_obj.value else "False"

        return ExprObj(value=test_obj.value, expressions=test_obj.expressions[:] + (condition,), type=test_obj.type)
