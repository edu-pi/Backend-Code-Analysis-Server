import ast

from app.visualize.analysis.element_manager import CodeElementManager
from app.visualize.analysis.stmt.expr.expr_traveler import ExprTraveler
from app.visualize.analysis.stmt.model.for_stmt_obj import BodyObj
from app.visualize.analysis.stmt.model.if_stmt_obj import ElseConditionObj, IfStmtObj, ConditionObj
from app.visualize.analysis.stmt.parser.assign_stmt import AssignStmt
from app.visualize.analysis.stmt.parser.expr_stmt import ExprStmt
from app.visualize.analysis.stmt.parser.for_stmt import ForStmt
from app.visualize.analysis.stmt.parser.if_stmt import IfStmt


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

        elif isinstance(node, ast.If):
            return StmtTraveler.if_travel(node, [], [], elem_manager)
        else:
            raise TypeError(f"[StmtTraveler] {type(node)}는 잘못된 타입입니다.")

    @staticmethod
    def if_travel(
        node: ast.If, conditions: list[ConditionObj], body_objs: list[BodyObj], elem_manager: CodeElementManager
    ) -> IfStmtObj:
        # parse 조건문 : if("test") or elfi("test") 부분
        StmtTraveler._append_condition_obj(conditions, elem_manager, node)

        # parse body
        StmtTraveler._parse_if_body(node, conditions, body_objs, elem_manager)

        # parse elif or else
        StmtTraveler._parse_if_orelse(body_objs, conditions, elem_manager, node)

        return IfStmtObj(conditions=tuple(conditions), body=BodyObj(body_steps=body_objs, cur_value=0))

    @staticmethod
    def _append_condition_obj(conditions, elem_manager, node: ast.If | ast.stmt):
        if len(conditions) == 0:  # if
            condition = IfStmt.parse_if_condition(node.test, elem_manager)

        elif isinstance(node, ast.If):  # elif
            condition = IfStmt.parse_elif_condition(node.test, elem_manager)

        else:
            raise TypeError(f"[IfTraveler] {type(node)}는 잘못된 타입입니다.")

        conditions.append(condition)

    @staticmethod
    def _append_else_condition_obj(conditions, node: ast.stmt, result: bool):
        if isinstance(node, ast.stmt):  # else
            condition = IfStmt.parse_else_condition(node, result)

        else:
            raise TypeError(f"[IfTraveler] {type(node)}는 잘못된 타입입니다.")

        conditions.append(condition)

    @staticmethod
    def _parse_if_body(
        node: ast.If, conditions: list[ConditionObj], body_objs: list[BodyObj], elem_manager: CodeElementManager
    ):
        if conditions[-1].result is True:  # 조건절의 결과 값이 True이면 해당 body 로직 추가
            for body in node.body:
                body_objs.append(StmtTraveler._internal_travel(body, elem_manager))

    @staticmethod
    def _parse_if_orelse(body_objs, conditions, elem_manager, node):
        # elif 처리
        if isinstance(node.orelse[0], ast.If):
            StmtTraveler.if_travel(node.orelse[0], conditions, body_objs, elem_manager)

        # else 처리
        elif isinstance(node.orelse[0], ast.stmt):
            if len(body_objs) == 0: # if, elif문 들의 조건 값이 모두 false 일 때 else문 의 body 추가
                StmtTraveler._append_else_condition_obj(conditions, node.orelse[0], True)
            else:
                StmtTraveler._append_else_condition_obj(conditions, node.orelse[0], False)

            for stmt_node in node.orelse:
                body_objs.append(StmtTraveler._internal_travel(stmt_node, elem_manager))

        else:
            raise TypeError(f"[IfTraveler] {type(node.orelse[0])}는 잘못된 타입입니다.")


