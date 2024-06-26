import ast

from app.visualize.analysis.element_manager import CodeElementManager
from app.visualize.analysis.stmt_parser.expr_analysis.expr_traveler import ExprTraveler


class AssignParser:

    @staticmethod
    def parse(targets: list[ast], value: ast, elem_manager: CodeElementManager):
        # a = b = "c + 1" -> "2 + 1" -> "3"
        # d = "3", d = 3
        # (a, b) = 2, 3
        return
