import ast

from app.visualize.analysis.element_manager import CodeElementManager
from app.visualize.analysis.stmt.expr.expr_traveler import ExprTraveler


class ExprStmt:

    @staticmethod
    def parse(expr_value: ast, elem_manager: CodeElementManager):
        return ExprStmt._get_parse_value(expr_value, elem_manager)

    @staticmethod
    def _get_parse_value(expr_value: ast, elem_manager: CodeElementManager):
        if isinstance(expr_value, ast.Name):
            return
        elif isinstance(expr_value, ast.Constant):
            return
        elif isinstance(expr_value, ast.BinOp):
            return
        elif isinstance(expr_value, ast.Call):
            return ExprTraveler.call_travel(expr_value, elem_manager)
        elif isinstance(expr_value, ast.Lambda):
            return
        else:
            raise TypeError(f"[ExprParser]:{type(expr_value)}는 정의되지 않았습니다.")
