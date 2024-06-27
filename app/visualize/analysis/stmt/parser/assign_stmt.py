import ast
from dataclasses import dataclass

from app.visualize.analysis.element_manager import CodeElementManager
from app.visualize.analysis.stmt.expr.expr_traveler import ExprTraveler


class AssignStmt:

    @staticmethod
    def parse(target_nodes: list[ast], value_node: ast, elem_manager: CodeElementManager):
        target_names = [AssignStmt._get_target_names(target_node, elem_manager) for target_node in target_nodes]
        expr_obj = AssignStmt._change_node_to_expr_obj(value_node, elem_manager)

        AssignStmt._assign_value_to_target(target_names, expr_obj.value, elem_manager)

        return

    @staticmethod
    def _get_target_names(node: ast, elem_manager: CodeElementManager):
        if isinstance(node, ast.Name):
            expr_obj = ExprTraveler.name_travel(node, elem_manager)

        else:
            raise TypeError(f"[AssignParser] {type(node)}는 잘못된 타입입니다.")

        return expr_obj.value

    @staticmethod
    def _change_node_to_expr_obj(node: ast, elem_manager: CodeElementManager):
        if isinstance(node, ast.BinOp):
            return ExprTraveler.binop_travel(node, elem_manager)

        elif isinstance(node, ast.Name):
            return ExprTraveler.name_travel(node, elem_manager)

        elif isinstance(node, ast.Constant):
            return ExprTraveler.constant_travel(node)

        else:
            raise TypeError(f"[AssignParser] {type(node)}는 잘못된 타입입니다.")

    @staticmethod
    def _assign_value_to_target(target_names: list[str], value, elem_manager: CodeElementManager):
        for target_name in target_names:
            elem_manager.add_variable_value(target_name, value)

    @staticmethod
    def _create_assign_obj(target_names: list[str], value_expressions: list[str]):
        assign_objs = []
        for value_expression in value_expressions:

            for target_name in target_names:
                assign_objs.append(AssignObj(target=target_name, value=value_expression))

        return assign_objs


@dataclass
class AssignObj:
    target: str
    value: str
    type: str = "assign"
