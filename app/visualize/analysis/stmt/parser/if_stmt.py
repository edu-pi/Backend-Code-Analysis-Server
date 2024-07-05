import ast

from app.visualize.analysis.element_manager import CodeElementManager
from app.visualize.analysis.stmt.expr.expr_traveler import ExprTraveler
from app.visualize.analysis.stmt.model.if_stmt_obj import ElseConditionObj, IfOrElifConditionObj


class IfStmt:

    @staticmethod
    def parse_condition(test_node: ast.expr, elem_manager: CodeElementManager):
        return IfOrElifConditionObj(
            expr_obj=ExprTraveler.travel(test_node, elem_manager),
            id=test_node.lineno,
            result=IfStmt._evaluate_test_value(test_node, elem_manager),
        )

    @staticmethod
    def parse_else_condition(else_body_node: ast.stmt):
        return ElseConditionObj(id=else_body_node.lineno - 1, result=False)

    @staticmethod
    def _evaluate_test_value(test_node: ast.expr, elem_manager: CodeElementManager):
        """
        Returns: 조건 절의 코드 실행 결과 반환
        """
        test_code = ast.unparse(test_node)
        return eval(test_code, elem_manager.get_element_dict())
