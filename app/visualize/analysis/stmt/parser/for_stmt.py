import ast

from app.visualize.container.element_container import ElementContainer
from app.visualize.analysis.stmt.expr.expr_traveler import ExprTraveler
from app.visualize.analysis.stmt.models.for_stmt_obj import ForStmtObj


class ForStmt:

    @staticmethod
    def parse(node: ast.For, elem_manager: ElementContainer):
        target_name = ForStmt._get_target_name(node.target, elem_manager)
        iter_obj = ForStmt._get_condition_obj(node.iter, elem_manager)

        return ForStmtObj(id=node.lineno, target_name=target_name, iter_obj=iter_obj)

    @staticmethod
    def _get_target_name(target, elem_manager: ElementContainer):
        if isinstance(target, ast.Name):
            name_obj = ExprTraveler.travel(target, elem_manager)
            return name_obj.value

        else:
            raise TypeError(f"[ForParser]:  {type(target)}는 잘못된 타입입니다.")

    @staticmethod
    def _get_condition_obj(iter: ast, elem_manager: ElementContainer):
        if isinstance(iter, ast.Call):
            range_obj = ExprTraveler.travel(iter, elem_manager)
            return range_obj

        elif isinstance(iter, ast.List):
            raise NotImplementedError(f"[ForParser]: {type(iter)}는 지원하지 않는 타입입니다.")

        else:
            raise TypeError(f"[ForParser]:  {type(iter)}는 잘못된 타입입니다.")
