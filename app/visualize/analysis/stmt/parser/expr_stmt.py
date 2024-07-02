import ast

from app.visualize.analysis.element_manager import CodeElementManager
from app.visualize.analysis.stmt.expr.expr_traveler import ExprTraveler
from app.visualize.analysis.stmt.model.expr_stmt_obj import ExprStmtObj


class ExprStmt:

    @staticmethod
    def parse(node: ast.Expr, elem_manager: CodeElementManager):
        expr_obj = ExprStmt._get_expr_obj(node.value, elem_manager)
        return ExprStmtObj(expr_obj=expr_obj, id=node.lineno)

    @staticmethod
    def _get_expr_obj(node_value: ast, elem_manager: CodeElementManager):
        if isinstance(node_value, ast.Name):
            name_obj = ExprTraveler.name_travel(node_value, elem_manager)
            return name_obj

        elif isinstance(node_value, ast.Constant):
            constant_obj = ExprTraveler.constant_travel(node_value)
            return constant_obj

        elif isinstance(node_value, ast.BinOp):
            binop_obj = ExprTraveler.binop_travel(node_value, elem_manager)
            return binop_obj

        elif isinstance(node_value, ast.Call):
            call_obj = ExprTraveler.call_travel(node_value, elem_manager)
            return call_obj

        elif isinstance(node_value, ast.Lambda):
            raise NotImplementedError(f"[ExprParser]:{type(node_value)}는 정의되지 않았습니다.")

        elif isinstance(node_value, ast.Compare):
            compare_obj = ExprTraveler.compare_travel(node_value, elem_manager)
            return compare_obj
        else:
            raise TypeError(f"[ExprParser]:{type(node_value)}는 지원하지 않습니다.")
