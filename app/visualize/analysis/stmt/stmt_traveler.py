import ast

from app.visualize.analysis.stmt.models.assign_stmt_obj import AssignStmtObj
from app.visualize.analysis.stmt.models.flow_control_obj import BreakStmtObj, ContinueStmtObj
from app.visualize.analysis.stmt.models.for_stmt_obj import BodyObj
from app.visualize.analysis.stmt.models.if_stmt_obj import IfStmtObj, ConditionObj
from app.visualize.analysis.stmt.models.return_stmt_obj import ReturnStmtObj
from app.visualize.analysis.stmt.models.user_func_stmt_obj import UserFuncStmtObj
from app.visualize.analysis.stmt.models.while_stmt_obj import WhileCycle, WhileStmtObj
from app.visualize.analysis.stmt.parser.assign_stmt import AssignStmt
from app.visualize.analysis.stmt.parser.expr.models.expr_obj import UserFunc, ExprObj
from app.visualize.analysis.stmt.parser.expr.models.expr_type import ExprType
from app.visualize.analysis.stmt.parser.expr_stmt import ExprStmt
from app.visualize.analysis.stmt.parser.flow_control_stmt import PassStmt, BreakStmt, ContinueStmt
from app.visualize.analysis.stmt.parser.for_stmt import ForStmt
from app.visualize.analysis.stmt.parser.func_def_stmt import FuncDefStmt
from app.visualize.analysis.stmt.parser.if_stmt import IfStmt
from app.visualize.analysis.stmt.parser.return_stmt import ReturnStmt
from app.visualize.analysis.stmt.parser.while_stmt import WhileStmt
from app.visualize.container.element_container import ElementContainer


class StmtTraveler:

    @staticmethod
    def travel(node: ast, elem_container: ElementContainer):
        if isinstance(node, ast.Assign):
            return StmtTraveler._assign_travel(node, elem_container)

        elif isinstance(node, ast.For):
            return StmtTraveler._for_travel(node, elem_container)

        elif isinstance(node, ast.Expr):
            return StmtTraveler._expr_travel(node, elem_container)

        elif isinstance(node, ast.If):
            return StmtTraveler._if_travel(node, [], [], elem_container)

        elif isinstance(node, ast.Pass | ast.Break | ast.Continue):
            return StmtTraveler._flow_control_travel(node)

        elif isinstance(node, ast.Return):
            return StmtTraveler._return_travel(node, elem_container)

        elif isinstance(node, ast.While):
            return StmtTraveler._while_travel(node, elem_container)

        elif isinstance(node, ast.FunctionDef):
            return StmtTraveler._func_def_travel(node, elem_container)

        else:
            raise TypeError(f"[StmtTraveler] {type(node)}는 잘못된 타입입니다.")

    @staticmethod
    def _assign_travel(node: ast.Assign, elem_container: ElementContainer):
        assign_obj = AssignStmt.parse(node, elem_container)
        expr_stmt_obj = assign_obj.expr_stmt_obj

        if expr_stmt_obj.expr_type is ExprType.USER_FUNC:
            user_func: UserFunc = expr_stmt_obj.value
            func_name: str = user_func.name
            func_signature: str = expr_stmt_obj.expressions
            body_asts: ast = user_func.user_func_ast
            args: dict = user_func.arguments

            local_elem_container = elem_container.make_local_elem_container(func_name, args)

            steps = [StmtTraveler.travel(body_ast, local_elem_container) for body_ast in body_asts]

            return_obj = None
            if isinstance(steps[-1], ReturnStmtObj):
                return_obj = steps[-1]

            AssignStmt.set_value_to_target(
                target_names=assign_obj.targets, expr_obj=return_obj, elem_container=elem_container
            )

            user_func_stmt_obj = UserFuncStmtObj(
                id=node.lineno,
                func_id=user_func.id,
                func_name=func_name,
                func_signature=func_signature,
                args=args,
                body_steps=steps,
                return_argument_name=assign_obj.targets[0],
                value=0 if return_obj is None else return_obj.value,
                expr=("",) if return_obj is None else return_obj.expr,
            )

            return AssignStmtObj(
                targets=assign_obj.targets,
                expr_stmt_obj=user_func_stmt_obj,
                call_stack_name=elem_container.get_call_stack_name(),
            )
        expr_stmt_obj = assign_obj.expr_stmt_obj
        expr_obj = ExprObj(
            value=expr_stmt_obj.value, expressions=expr_stmt_obj.expressions, type=expr_stmt_obj.expr_type
        )
        AssignStmt.set_value_to_target(assign_obj.targets, expr_obj, elem_container)

        return assign_obj

    @staticmethod
    def _for_travel(node: ast.For, elem_container: ElementContainer):
        # parse condition
        for_stmt_obj = ForStmt.parse(node, elem_container)

        # parse body
        body_objs = []

        for i in for_stmt_obj.iter_obj.value:
            # init value 값 변경
            elem_container.add_element(for_stmt_obj.target_name, i)
            # for문 안 body 로직을 stmt 리스트로 변환
            body_steps = StmtTraveler._parse_for_body(node.body, elem_container)

            # break 존재할 때
            if ForStmt.contain_flow_control(body_steps, BreakStmtObj):
                body_steps = ForStmt.get_pre_flow_control_body_steps(body_steps, BreakStmtObj)
                body_objs.append(BodyObj(cur_value=i, body_steps=body_steps))
                break

            # continue 존재할 때
            if ForStmt.contain_flow_control(body_steps, ContinueStmtObj):
                body_steps = ForStmt.get_pre_flow_control_body_steps(body_steps, ContinueStmtObj)
                body_objs.append(BodyObj(cur_value=i, body_steps=body_steps))
                continue

            body_objs.append(BodyObj(cur_value=i, body_steps=body_steps))

        for_stmt_obj.body_objs = body_objs
        return for_stmt_obj

    @staticmethod
    def _parse_for_body(bodies: list[ast.stmt], elem_container: ElementContainer):
        if not any(isinstance(body, ast.stmt) for body in bodies):
            raise TypeError("[StmtTraveler] for문의 body가 ast.stmt 타입이 아닙니다.")

        stmt_objs = [StmtTraveler.travel(body, elem_container) for body in bodies]

        return stmt_objs

    @staticmethod
    def _expr_travel(node: ast.Expr, elem_container: ElementContainer):
        expr_stmt_obj = ExprStmt.parse(node, elem_container)

        if expr_stmt_obj.expr_type is ExprType.USER_FUNC:
            user_func: UserFunc = expr_stmt_obj.value
            func_name: str = user_func.name
            func_signature: str = expr_stmt_obj.expressions
            body_asts: ast = user_func.user_func_ast
            args: dict = user_func.arguments

            local_elem_container = elem_container.make_local_elem_container(func_name, args)

            steps = [StmtTraveler.travel(body_ast, local_elem_container) for body_ast in body_asts]

            return_obj = None
            if isinstance(steps[-1], ReturnStmtObj):
                return_obj = steps[-1]

            return UserFuncStmtObj(
                id=node.lineno,
                func_id=user_func.id,
                func_name=func_name,
                func_signature=func_signature,
                args=args,
                body_steps=steps,
                return_argument_name="",
                value=0 if return_obj is None else return_obj.value,
                expr=("",) if return_obj is None else return_obj.expr,
            )

        return expr_stmt_obj

    @staticmethod
    def _if_travel(
        node: ast.If, conditions: list[ConditionObj], body_steps: list, elem_container: ElementContainer
    ) -> IfStmtObj:
        # parse 조건문 : if("test") or elfi("test") 부분
        StmtTraveler._append_condition_obj(conditions, elem_container, node)

        # parse body
        StmtTraveler._parse_if_body(node, conditions, body_steps, elem_container)

        # parse elif or else
        if isinstance(node, ast.If) and node.orelse:  # 빈 배열이면 탐색 안함
            StmtTraveler._parse_if_branches(body_steps, conditions, elem_container, node.orelse)

        return IfStmtObj(conditions=tuple(conditions), body_steps=body_steps)

    @staticmethod
    def _append_condition_obj(conditions, elem_container, node: ast.If | ast.stmt):
        if len(conditions) == 0:  # if
            condition = IfStmt.parse_if_condition(node.test, elem_container)

        elif isinstance(node, ast.If):  # elif
            condition = IfStmt.parse_elif_condition(node.test, elem_container)

        else:
            raise TypeError(f"[IfTraveler] {type(node)}는 잘못된 타입입니다.")

        # 조건문 parse: if("test") or elif("test") 부분
        conditions.append(condition)

    @staticmethod
    def _parse_if_body(
        node: ast.stmt, conditions: list[ConditionObj], body_objs: list[BodyObj], elem_container: ElementContainer
    ):
        if conditions[-1].result:  # 조건절의 결과 값이 True이면 해당 body 로직 추가
            for body in node.body:
                body_objs.append(StmtTraveler.travel(body, elem_container))

    @staticmethod
    def _parse_if_branches(body_steps, conditions, elem_container, orelse_node):
        # elif 처리
        if isinstance(orelse_node[0], ast.If):
            StmtTraveler._if_travel(orelse_node[0], conditions, body_steps, elem_container)

        # else 처리
        elif isinstance(orelse_node[0], ast.stmt):
            StmtTraveler._parse_else(orelse_node, conditions, body_steps, elem_container)

        else:
            raise TypeError(f"[IfTraveler] {type(orelse_node[0])}는 잘못된 타입입니다.")

    @staticmethod
    def _parse_else(nodes: list[ast.stmt], conditions, body_steps, elem_container):
        is_else_condition_true = True if len(body_steps) == 0 else False
        StmtTraveler._append_else_condition_obj(conditions, nodes[0], is_else_condition_true)

        if is_else_condition_true:
            # else 문의 body 추가
            for stmt_node in nodes:
                body_steps.append(StmtTraveler.travel(stmt_node, elem_container))

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

    @staticmethod
    def _return_travel(node: ast.Return, elem_container: ElementContainer):
        return ReturnStmt.parse(node, elem_container)

    @staticmethod
    def _while_travel(node: ast.While, elem_container: ElementContainer):
        while_cycles = []
        condition_value = True

        while condition_value:
            body_objs = []
            # ast.While의 조건문 파싱
            condition_obj = WhileStmt.parse_condition(node.test, elem_container)
            condition_value = condition_obj.value

            # 조건문이 False일 경우 body 로직을 탐색하지 않음
            if condition_value:
                body_objs = StmtTraveler._parse_for_body(node.body, elem_container)

            # 단계별로 while의 조건문 표현식과 body 로직을 저장
            while_cycles.append(WhileCycle(condition_exprs=condition_obj.expressions, body_objs=body_objs))

        # while의 else 로직을 저장
        while_else_objs = [StmtTraveler.travel(orelse, elem_container) for orelse in node.orelse]

        # id와 while의 결과를 저장한 객체 반환
        return WhileStmtObj(
            id=node.lineno,
            orelse=while_else_objs,
            while_cycles=while_cycles,
        )

    @staticmethod
    def _func_def_travel(node: ast.FunctionDef, elem_container: ElementContainer):
        return FuncDefStmt.parse(node, elem_container)
