import ast

from app.visualize.analysis.stmt.models.flowcontrolobj.break_stmt_obj import BreakStmtObj
from app.visualize.analysis.stmt.models.if_stmt_obj import IfStmtObj
from app.visualize.container.element_container import ElementContainer
from app.visualize.analysis.stmt.parser.expr.expr_traveler import ExprTraveler
from app.visualize.analysis.stmt.models.for_stmt_obj import ForStmtObj


class ForStmt:

    @staticmethod
    def parse(node: ast.For, elem_container: ElementContainer):
        target_name = ForStmt._get_target_name(node.target, elem_container)
        iter_obj = ForStmt._get_condition_obj(node.iter, elem_container)

        return ForStmtObj(id=node.lineno, target_name=target_name, iter_obj=iter_obj)

    @staticmethod
    def _get_target_name(target, elem_container: ElementContainer):
        if isinstance(target, ast.Name):
            name_obj = ExprTraveler.travel(target, elem_container)
            return name_obj.value

        else:
            raise TypeError(f"[ForParser]:  {type(target)}는 잘못된 타입입니다.")

    @staticmethod
    def _get_condition_obj(iter: ast, elem_container: ElementContainer):
        if isinstance(iter, ast.Call):
            range_obj = ExprTraveler.travel(iter, elem_container)
            return range_obj

        elif isinstance(iter, ast.List):
            raise NotImplementedError(f"[ForParser]: {type(iter)}는 지원하지 않는 타입입니다.")

        else:
            raise TypeError(f"[ForParser]:  {type(iter)}는 잘못된 타입입니다.")

    @staticmethod
    def contains_break(body_steps):
        for stmt in body_steps:
            if isinstance(stmt, IfStmtObj):
                return any(isinstance(step, BreakStmtObj) for step in stmt.body.body_steps)

            elif isinstance(stmt, BreakStmtObj):
                return True

        return False
