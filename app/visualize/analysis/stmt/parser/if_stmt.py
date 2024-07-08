import ast

from app.visualize.container.element_container import ElementContainer
from app.visualize.analysis.stmt.expr.expr_traveler import ExprTraveler
from app.visualize.analysis.stmt.models.if_stmt_obj import ElseConditionObj, IfConditionObj, ElifConditionObj


class IfStmt:

    @staticmethod
    def parse_if_condition(test_node: ast.expr, elem_container: ElementContainer):
        return IfConditionObj(
            id=test_node.lineno,
            expressions=ExprTraveler.travel(test_node, elem_container).expressions,
            result=IfStmt._evaluate_test_value(test_node, elem_container),
        )

    @staticmethod
    def parse_elif_condition(test_node: ast.expr, elem_container: ElementContainer):
        return ElifConditionObj(
            id=test_node.lineno,
            expressions=ExprTraveler.travel(test_node, elem_container).expressions,
            result=IfStmt._evaluate_test_value(test_node, elem_container),
        )

    @staticmethod
    def parse_else_condition(else_body_node: ast.stmt, result: bool):
        return ElseConditionObj(id=else_body_node.lineno - 1, expressions=None, result=result)

    @staticmethod
    def _evaluate_test_value(test_node: ast.expr, elem_container: ElementContainer):
        """
        Returns: 조건 절의 코드 실행 결과 반환
        """
        test_code = ast.unparse(test_node)
        return eval(test_code, elem_container.get_element_dict())
