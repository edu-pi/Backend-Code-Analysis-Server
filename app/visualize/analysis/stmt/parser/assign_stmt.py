import ast

from app.visualize.analysis.element_manager import CodeElementManager
from app.visualize.analysis.stmt.expr.expr_traveler import ExprTraveler
from app.visualize.analysis.stmt.model.assign_stmt_obj import AssignStmtObj


class AssignStmt:

    @staticmethod
    def parse(node: ast.Assign, elem_manager: CodeElementManager):
        target_names = [AssignStmt._get_target_name(target_node, elem_manager) for target_node in node.targets]
        expr_obj = AssignStmt._change_node_to_expr_obj(node.value, elem_manager)

        AssignStmt._set_value_to_target(target_names, expr_obj.value, elem_manager)

        return AssignStmtObj(
            id=node.lineno, targets=target_names, expressions=expr_obj.expressions, value=expr_obj.value
        )

    @staticmethod
    def _get_target_name(node: ast, elem_manager: CodeElementManager):
        if isinstance(node, ast.Name):
            expr_obj = ExprTraveler.name_travel(node, elem_manager)

        else:
            raise TypeError(f"[AssignParser]: {type(node)}는 잘못된 타입입니다.")

        return expr_obj.value

    @staticmethod
    def _change_node_to_expr_obj(node: ast, elem_manager: CodeElementManager):
        if isinstance(node, ast.BinOp):
            return ExprTraveler.binop_travel(node, elem_manager)

        elif isinstance(node, ast.Name):
            return ExprTraveler.name_travel(node, elem_manager)

        elif isinstance(node, ast.Constant):
            return ExprTraveler.constant_travel(node)

        elif isinstance(node, ast.List):
            return ExprTraveler.list_travel(node, elem_manager)

        else:
            raise TypeError(f"[AssignParser] {type(node)}는 잘못된 타입입니다.")

    @staticmethod
    def _set_value_to_target(target_names: list[str], value, elem_manager: CodeElementManager):
        for target_name in target_names:
            elem_manager.set_element(target_name, value)
