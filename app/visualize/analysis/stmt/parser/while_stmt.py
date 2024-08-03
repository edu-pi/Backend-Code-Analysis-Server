import ast
from dataclasses import replace

from app.visualize.analysis.stmt.models.while_stmt_obj import WhileStmtObj
from app.visualize.analysis.stmt.parser.expr.expr_traveler import ExprTraveler
from app.visualize.container.element_container import ElementContainer


class WhileStmt:

    @staticmethod
    def parse_condition(test_node: ast.expr, elem_container: ElementContainer):
        test_obj = ExprTraveler.travel(test_node, elem_container)
        return WhileStmt.add_last_bool_expression(test_obj)

    @staticmethod
    def parse(call_id, while_steps):
        return WhileStmtObj(
            id=call_id,
            while_cycles=while_steps,
        )

    # ast.if와 ast.while에서 조건절에 사용할 경우 마지막 표현식이 bool이 아니라면 bool 표현을 추가하는
    # ex) "" -> False, "hello" -> True
    @staticmethod
    def add_last_bool_expression(test_obj):
        # 마지막 표현식에 bool 표현이 이미 있는 경우
        if test_obj.expressions[-1] in ("True", "False"):
            return test_obj

        # 결과가 if문에서 true로 작동하면 "True" 추가, false로 작동하면 "False" 추가
        condition = "True" if test_obj.value else "False"
        return replace(test_obj, expressions=test_obj.expressions + (condition,))
