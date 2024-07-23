import ast

from app.visualize.analysis.stmt.models.flow_control_obj import BreakStmtObj
from app.visualize.analysis.stmt.models.if_stmt_obj import IfStmtObj
from app.visualize.analysis.stmt.parser.expr.models.expr_obj import ExprObj
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
    def _get_condition_obj(iter_node: ast, elem_container: ElementContainer) -> ExprObj:
        if isinstance(iter_node, ast.Call):
            call_obj = ExprTraveler.travel(iter_node, elem_container)
            return call_obj

        elif isinstance(iter_node, ast.List):
            list_obj = ExprTraveler.travel(iter_node, elem_container)
            return list_obj

        else:
            raise TypeError(f"[ForParser]:  {type(iter)}는 잘못된 타입입니다.")

    @staticmethod
    def contains_break(body_objs):
        for stmt_obj in body_objs:
            if isinstance(stmt_obj, IfStmtObj):
                if ForStmt.contains_break(stmt_obj.body_steps):
                    return True

            elif isinstance(stmt_obj, BreakStmtObj):
                return True

        return False

    @staticmethod
    def get_pre_break_body_steps(body_objs) -> list:
        result = []

        for stmt_obj in body_objs:
            # break 발견 후 중단
            if isinstance(stmt_obj, BreakStmtObj):
                result.append(stmt_obj)
                break

            if isinstance(stmt_obj, IfStmtObj):
                # if문 안에 break 존재할 때
                if ForStmt.contains_break(stmt_obj.body_steps):
                    # break 이후를 제외한 스텝 생성
                    new_body = ForStmt.get_pre_break_body_steps(stmt_obj.body_steps)
                    # 새로운 if_stmt 객체 생성 후 삽입
                    result.append(stmt_obj.create_with_new_body(new_body))
                    break

            result.append(stmt_obj)

        return result
