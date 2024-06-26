import ast

from app.visualize.analysis.element_manager import CodeElementManager
from app.visualize.analysis.stmt_parser.expr_parser import ExprParser
from app.visualize.analysis.stmt_parser.for_parser import ForParser


class StmtTraveler:

    @staticmethod
    def for_travel(node: ast.For, elem_manager: CodeElementManager):
        for_info = ForParser.parse(node.target, node.iter, elem_manager)
        # body
        start, end, step = for_info["condition_dict"]["value"]
        for i in range(start, end, step):
            for body in node.body:
                StmtTraveler._internal_travel(body, elem_manager)

    @staticmethod
    def expr_travel(node: ast.Expr, elem_manager: CodeElementManager):
        return ExprParser.parse(node.value, elem_manager)

    @staticmethod
    def _internal_travel(node: ast, elem_manager: CodeElementManager):
        if isinstance(node, ast.For):
            return StmtTraveler.for_travel(node, elem_manager)

        elif isinstance(node, ast.Expr):
            return StmtTraveler.expr_travel(node, elem_manager)
        else:
            raise TypeError(f"[StmtTraveler] {type(node)}는 잘못된 타입입니다.")
