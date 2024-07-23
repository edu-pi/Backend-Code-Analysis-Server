import ast

from app.visualize.analysis.stmt.models.flow_control_obj import BreakStmtObj
from app.visualize.analysis.stmt.parser.flow_control_stmt import PassStmt, BreakStmt, ContinueStmt
from app.visualize.container.element_container import ElementContainer
from app.visualize.analysis.stmt.models.for_stmt_obj import BodyObj
from app.visualize.analysis.stmt.models.if_stmt_obj import IfStmtObj, ConditionObj
from app.visualize.analysis.stmt.parser.assign_stmt import AssignStmt
from app.visualize.analysis.stmt.parser.expr_stmt import ExprStmt
from app.visualize.analysis.stmt.parser.for_stmt import ForStmt
from app.visualize.analysis.stmt.parser.if_stmt import IfStmt


class StmtTraveler:

    @staticmethod
    def travel(node: ast, elem_manager: ElementContainer):
        if isinstance(node, ast.Assign):
            return StmtTraveler._assign_travel(node, elem_manager)

        elif isinstance(node, ast.For):
            return StmtTraveler._for_travel(node, elem_manager)

        elif isinstance(node, ast.Expr):
            return StmtTraveler._expr_travel(node, elem_manager)

        elif isinstance(node, ast.If):
            return StmtTraveler._if_travel(node, [], [], elem_manager)

        elif isinstance(node, ast.Pass | ast.Break | ast.Continue):
            return StmtTraveler._flow_control_travel(node)

        else:
            raise TypeError(f"[StmtTraveler] {type(node)}는 잘못된 타입입니다.")

    @staticmethod
    def _assign_travel(node: ast.Assign, elem_manager: ElementContainer):
        return AssignStmt.parse(node, elem_manager)

    @staticmethod
    def _for_travel(node: ast.For, elem_manager: ElementContainer):
        # parse condition
        for_stmt_obj = ForStmt.parse(node, elem_manager)

        # parse body
        body_objs = []
        is_break = False

        for i in for_stmt_obj.iter_obj.value:
            # init value 값 변경
            elem_manager.set_element(for_stmt_obj.target_name, i)
            body_steps = StmtTraveler._parse_for_body(node.body, elem_manager)

            if ForStmt.contain_flow_control(body_steps, BreakStmtObj):
                body_steps = ForStmt.get_pre_break_body_steps(body_steps)
                is_break = True

            body_objs.append(BodyObj(cur_value=i, body_steps=body_steps))

            if is_break:
                break

        for_stmt_obj.body_objs = body_objs
        return for_stmt_obj

    @staticmethod
    def _parse_for_body(bodies: list[ast.stmt], elem_manager: ElementContainer):
        if not any(isinstance(body, ast.stmt) for body in bodies):
            raise TypeError("[StmtTraveler] for문의 body가 ast.stmt 타입이 아닙니다.")

        stmt_objs = [StmtTraveler.travel(body, elem_manager) for body in bodies]

        return stmt_objs

    @staticmethod
    def _expr_travel(node: ast.Expr, elem_manager: ElementContainer):
        return ExprStmt.parse(node, elem_manager)

    @staticmethod
    def _if_travel(
        node: ast.If, conditions: list[ConditionObj], body_steps: list, elem_manager: ElementContainer
    ) -> IfStmtObj:
        # parse 조건문 : if("test") or elfi("test") 부분
        StmtTraveler._append_condition_obj(conditions, elem_manager, node)

        # parse body
        StmtTraveler._parse_if_body(node, conditions, body_steps, elem_manager)

        # parse elif or else
        if isinstance(node, ast.If) and node.orelse:  # 빈 배열이면 탐색 안함
            StmtTraveler._parse_if_branches(body_steps, conditions, elem_manager, node.orelse)

        return IfStmtObj(conditions=tuple(conditions), body_steps=body_steps)

    @staticmethod
    def _append_condition_obj(conditions, elem_manager, node: ast.If | ast.stmt):
        if len(conditions) == 0:  # if
            condition = IfStmt.parse_if_condition(node.test, elem_manager)

        elif isinstance(node, ast.If):  # elif
            condition = IfStmt.parse_elif_condition(node.test, elem_manager)

        else:
            raise TypeError(f"[IfTraveler] {type(node)}는 잘못된 타입입니다.")

        # 조건문 parse: if("test") or elif("test") 부분
        conditions.append(condition)

    @staticmethod
    def _parse_if_body(
        node: ast.stmt, conditions: list[ConditionObj], body_objs: list[BodyObj], elem_manager: ElementContainer
    ):
        if conditions[-1].result is True:  # 조건절의 결과 값이 True이면 해당 body 로직 추가
            for body in node.body:
                body_objs.append(StmtTraveler.travel(body, elem_manager))

    @staticmethod
    def _parse_if_branches(body_steps, conditions, elem_manager, orelse_node):
        # elif 처리
        if isinstance(orelse_node[0], ast.If):
            StmtTraveler._if_travel(orelse_node[0], conditions, body_steps, elem_manager)

        # else 처리
        elif isinstance(orelse_node[0], ast.stmt):
            StmtTraveler._parse_else(orelse_node, conditions, body_steps, elem_manager)

        else:
            raise TypeError(f"[IfTraveler] {type(orelse_node[0])}는 잘못된 타입입니다.")

    @staticmethod
    def _parse_else(nodes: list[ast.stmt], conditions, body_steps, elem_manager):
        is_else_condition_true = True if len(body_steps) == 0 else False
        StmtTraveler._append_else_condition_obj(conditions, nodes[0], is_else_condition_true)

        if is_else_condition_true:
            # else 문의 body 추가
            for stmt_node in nodes:
                body_steps.append(StmtTraveler.travel(stmt_node, elem_manager))

    @staticmethod
    def _append_else_condition_obj(conditions, node: ast.stmt, result: bool):
        if isinstance(node, ast.stmt):  # else
            condition = IfStmt.parse_else_condition(node, result)

        else:
            raise TypeError(f"[IfTraveler] {type(node)}는 잘못된 타입입니다.")

        conditions.append(condition)

    @staticmethod
    def _flow_control_travel(node: ast.Pass | ast.Break | ast.Continue):
        if isinstance(node, ast.Pass):
            return PassStmt.parse(node)

        elif isinstance(node, ast.Break):
            return BreakStmt.parse(node)

        elif isinstance(node, ast.Continue):
            return ContinueStmt.parse(node)

        else:
            raise TypeError(f"[FlowControlTravel] {type(node)}는 잘못된 타입입니다.")
