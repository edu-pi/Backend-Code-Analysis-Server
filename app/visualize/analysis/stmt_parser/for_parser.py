import ast

from app.visualize.analysis.element_manager import CodeElementManager
from app.visualize.analysis.stmt_parser.expr_analysis.expr_traveler import ExprTraveler


class ForParser:
    @staticmethod
    def parse(target: ast, iter: ast, elem_manager: CodeElementManager):
        target_name = ForParser._get_target_name(target, elem_manager)
        condition_dict = ForParser._get_condition_value_list(iter, elem_manager)

        return {"target": target_name, "condition_dict": condition_dict}

    @staticmethod
    def _get_target_name(target, elem_manager: CodeElementManager):
        if isinstance(target, ast.Name):
            return ExprTraveler.name_travel(target, elem_manager)

        else:
            raise TypeError(f"[ForParser]:  {type(target)}는 잘못된 타입입니다.")

    @staticmethod
    def _get_condition_value_list(iter: ast, elem_manager: CodeElementManager):
        if isinstance(iter, ast.Call):
            # {value: {start: 3, end: 10, step: 2}, expressions: [{start: a, end: 10, step: 2}...{start: 3, end: 10, step: 2}]
            return ExprTraveler.call_travel(iter, elem_manager)

        elif isinstance(iter, ast.List):
            return

        else:
            raise TypeError(f"[ForParser]:  {type(iter)}는 잘못된 타입입니다.")
