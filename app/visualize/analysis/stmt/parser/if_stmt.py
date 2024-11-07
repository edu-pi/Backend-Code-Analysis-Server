import ast
from dataclasses import replace

from app.visualize.analysis.stmt.models.if_stmt_obj import ElseConditionObj, IfConditionObj, ElifConditionObj
from app.visualize.analysis.stmt.parser.expr.expr_traveler import ExprTraveler
from app.visualize.container.element_container import ElementContainer


class IfStmt:

    @staticmethod
    def parse_if_condition(test_node: ast.expr, elem_container: ElementContainer):
        test_obj = ExprTraveler.travel(test_node, elem_container)
        test_obj = IfStmt._add_last_bool_expression(test_obj)

        return IfConditionObj(
            id=test_node.lineno,
            expressions=test_obj.expressions,
            result=test_obj.value,
        )

    @staticmethod
    def parse_elif_condition(test_node: ast.expr, elem_container: ElementContainer):
        test_obj = ExprTraveler.travel(test_node, elem_container)
        IfStmt._add_last_bool_expression(test_obj)

        return ElifConditionObj(
            id=test_node.lineno,
            expressions=test_obj.expressions,
            result=test_obj.value,
        )

    @staticmethod
    def parse_else_condition(else_body_node: ast.stmt, result: bool):
        return ElseConditionObj(id=else_body_node.lineno - 1, expressions=("True",), result=result)

    # ast.if와 ast.while에서 조건절에 사용할 경우 마지막 표현식이 bool이 아니라면 bool 표현을 추가하는
    # ex) "" -> False, "hello" -> True
    @staticmethod
    def _add_last_bool_expression(test_obj):
        # 마지막 표현식에 bool 표현이 이미 있는 경우
        if test_obj.expressions[-1] in ("True", "False"):
            return test_obj

        # 결과가 if문에서 true로 작동하면 "True" 추가, false로 작동하면 "False" 추가
        condition = "True" if test_obj.value else "False"
        return replace(test_obj, expressions=test_obj.expressions + (condition,))
