import ast

from app.visualize.analysis.element_manager import CodeElementManager
from app.visualize.analysis.stmt.expr.expr_traveler import ExprTraveler
from app.visualize.analysis.stmt.model.if_stmt_obj import ElseConditionObj, IfConditionObj, ElifConditionObj


class IfStmt:

    @staticmethod
    def parse_if_condition(test_node: ast.expr, elem_manager: CodeElementManager):
        return IfConditionObj(
            id=test_node.lineno,
            expressions=ExprTraveler.travel(test_node, elem_manager).expressions,
            result=IfStmt._evaluate_test_value(test_node, elem_manager),
        )

    @staticmethod
    def parse_elif_condition(test_node: ast.expr, elem_manager: CodeElementManager):
        return ElifConditionObj(
            id=test_node.lineno,
            expressions=ExprTraveler.travel(test_node, elem_manager).expressions,
            result=IfStmt._evaluate_test_value(test_node, elem_manager),
        )

    @staticmethod
    def parse_else_condition(else_body_node: ast.stmt, result: bool):
        return ElseConditionObj(id=else_body_node.lineno - 1, expressions=None, result=result)

    @staticmethod
    def _evaluate_test_value(test_node: ast.expr, elem_manager: CodeElementManager):
        """
        Returns: 조건 절의 코드 실행 결과 반환
        """
        test_code = ast.unparse(test_node)
        return eval(test_code, elem_manager.get_element_dict())
