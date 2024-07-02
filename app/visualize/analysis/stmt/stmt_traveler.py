import ast

from app.visualize.analysis.element_manager import CodeElementManager
from app.visualize.analysis.stmt.model.for_stmt_obj import BodyObj
from app.visualize.analysis.stmt.parser.assign_stmt import AssignStmt
from app.visualize.analysis.stmt.parser.expr_stmt import ExprStmt
from app.visualize.analysis.stmt.parser.for_stmt import ForStmt


class StmtTraveler:

    @staticmethod
    def assign_travel(node: ast.Assign, elem_manager: CodeElementManager):
        return AssignStmt.parse(node, elem_manager)

    @staticmethod
    def for_travel(node: ast.For, elem_manager: CodeElementManager):
        # parse condition
        for_stmt_obj = ForStmt.parse(node, elem_manager)

        # parse body
        body_objs = []

        for i in for_stmt_obj.iter_obj.value:
            # init value 값 변경
            elem_manager.set_element(for_stmt_obj.target_name, i)
            body_steps = []

            for body in node.body:
                body_steps.append(StmtTraveler._internal_travel(body, elem_manager))

            body_objs.append(BodyObj(cur_value=i, body_steps=body_steps))

        for_stmt_obj.body_objs = body_objs

        return for_stmt_obj

    @staticmethod
    def expr_travel(node: ast.Expr, elem_manager: CodeElementManager):
        return ExprStmt.parse(node, elem_manager)

    @staticmethod
    def _internal_travel(node: ast, elem_manager: CodeElementManager):

        if isinstance(node, ast.Assign):
            return StmtTraveler.assign_travel(node, elem_manager)

        elif isinstance(node, ast.For):
            return StmtTraveler.for_travel(node, elem_manager)

        elif isinstance(node, ast.Expr):
            return StmtTraveler.expr_travel(node, elem_manager)

        else:
            raise TypeError(f"[StmtTraveler] {type(node)}는 잘못된 타입입니다.")



    @staticmethod
    def if_travel(node: ast.If, tests: list, elem_manager: CodeElementManager):
        pass
        # test - if("test") or elfi("test") 부분
        tests.append(StmtTraveler._internal_travel(node.test, elem_manager))

        # body

        # orelse

