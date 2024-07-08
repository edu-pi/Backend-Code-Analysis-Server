import ast

from app.visualize.container.element_container import ElementContainer
from app.visualize.analysis.stmt.expr.expr_traveler import ExprTraveler
from app.visualize.analysis.stmt.models.assign_stmt_obj import AssignStmtObj
from app.visualize.analysis.stmt.models.expr_stmt_obj import ExprStmtObj


class AssignStmt:

    @staticmethod
    def parse(node: ast.Assign, elem_container: ElementContainer):
        target_names = tuple(AssignStmt._get_target_name(target_node, elem_container) for target_node in node.targets)
        expr_obj = AssignStmt._change_node_to_expr_obj(node.value, elem_container)

        AssignStmt._set_value_to_target(target_names, expr_obj, elem_container)

        return AssignStmtObj(
            targets=target_names,
            expr_stmt_obj=ExprStmtObj(
                id=node.lineno,
                expressions=expr_obj.expressions,
                value=expr_obj.value,
                expr_type=expr_obj.type,
            ),
        )

    @staticmethod
    def _get_target_name(node: ast, elem_container: ElementContainer):
        if isinstance(node, ast.Name):
            expr_obj = ExprTraveler.travel(node, elem_container)

        else:
            raise TypeError(f"[AssignParser]: {type(node)}는 잘못된 타입입니다.")

        return expr_obj.value

    @staticmethod
    def _change_node_to_expr_obj(node: ast, elem_container: ElementContainer):
        return ExprTraveler.travel(node, elem_container)

    @staticmethod
    def _set_value_to_target(target_names: tuple[str, ...], expr_obj, elem_container: ElementContainer):
        for target_name in target_names:
            value = expr_obj.value

            if expr_obj.type == "list":
                value = list(expr_obj.value)

            elem_container.set_element(target_name, value)
