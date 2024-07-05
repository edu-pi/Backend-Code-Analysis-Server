import ast

from app.visualize.analysis.element_manager import CodeElementManager
from app.visualize.analysis.stmt.expr.expr_traveler import ExprTraveler
from app.visualize.analysis.stmt.model.if_stmt_obj import ElseConditionObj, IfOrElifConditionObj


class IfStmt:

    @staticmethod
    def parse_condition(test_node: ast.expr, elem_manager: CodeElementManager):
        # Todo: ExprTraveler의 travel 함수가 만들어지면 변경할 에정
        if isinstance(test_node, ast.Compare):
            expr_obj = ExprTraveler.travel(test_node, elem_manager)

        return IfOrElifConditionObj(
            expr_obj=expr_obj,
            id=test_node.lineno,
            result=IfStmt._evaluate_test_value(test_node, elem_manager),
        )

    @staticmethod
    def parse_else_condition(orelse_node):
        return ElseConditionObj(id=orelse_node.lineno - 1, result=False)

    @staticmethod
    def _evaluate_test_value(test_node: ast.expr, elem_manager: CodeElementManager):
        test_code = ast.unparse(test_node)
        return eval(test_code, elem_manager.get_element_dict())
