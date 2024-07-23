import ast

from app.visualize.analysis.stmt.parser.expr.models.expr_type import ExprType
from app.visualize.container.element_container import ElementContainer
from app.visualize.analysis.stmt.parser.expr.expr_traveler import ExprTraveler
from app.visualize.analysis.stmt.models.assign_stmt_obj import AssignStmtObj
from app.visualize.analysis.stmt.models.expr_stmt_obj import ExprStmtObj


class AssignStmt:

    @staticmethod
    def parse(node: ast.Assign, elem_container: ElementContainer):
        target_names = AssignStmt._get_target_names(node.targets, elem_container)
        expr_obj = AssignStmt._change_node_to_expr_obj(node.value, elem_container)

        AssignStmt._set_value_to_target(target_names, expr_obj, elem_container)

        expr_stmt_obj = ExprStmtObj(
            id=node.lineno,
            expressions=expr_obj.expressions,
            value=expr_obj.value,
            expr_type=expr_obj.type,
        )

        return AssignStmtObj(targets=target_names, expr_stmt_obj=expr_stmt_obj)

    @staticmethod
    def _get_target_names(target_nodes: list[ast], elem_container: ElementContainer):
        target_names = []

        for target_node in target_nodes:
            if isinstance(target_node, ast.Name):
                expr_obj = ExprTraveler.travel(target_node, elem_container)

            elif isinstance(target_node, ast.Tuple):
                expr_obj = ExprTraveler.travel(target_node, elem_container)

            elif isinstance(target_node, ast.List):
                expr_obj = ExprTraveler.travel(target_node, elem_container)

            else:
                raise TypeError(f"[AssignParser]: {type(target_node)}는 잘못된 타입입니다.")

            target_names.append(expr_obj.value)

        return tuple(target_names)

    @staticmethod
    def _change_node_to_expr_obj(node: ast, elem_container: ElementContainer):
        return ExprTraveler.travel(node, elem_container)

    @staticmethod
    def _set_value_to_target(target_names: tuple, expr_obj, elem_container: ElementContainer):
        for target_name in target_names:
            value = expr_obj.value

            if expr_obj.type is ExprType.LIST:
                value = list(expr_obj.value)

            elif expr_obj.type is ExprType.TUPLE:
                value = tuple(expr_obj.value)

            elem_container.set_element(target_name, value)
