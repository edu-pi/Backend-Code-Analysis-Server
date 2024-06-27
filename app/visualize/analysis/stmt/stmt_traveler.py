import ast

from app.visualize.analysis.element_manager import CodeElementManager
from app.visualize.analysis.stmt.model.for_stmt_obj import ForStmtObj
from app.visualize.analysis.stmt.parser.expr_stmt import ExprStmt
from app.visualize.analysis.stmt.parser.for_stmt import ForStmt


class StmtTraveler:

    @staticmethod
    def for_travel(node: ast.For, elem_manager: CodeElementManager):
        # parse condition
        for_stmt_obj = ForStmt.parse(node.target, node.iter, elem_manager)
        # parse body
        body_odjs = []
        init_value = for_stmt_obj.init_value
        condition = for_stmt_obj.condition

        if condition.type == "range":
            # 파싱한 제어문대로 body를 파싱하는 Loop 시작
            for i in range(condition.value["start"], condition.value["end"], condition.value["step"]):
                # init value 값 변경
                elem_manager.set_element(init_value.value, i)
                for body in node.body:
                    # parse body
                    body_odjs.append(StmtTraveler._internal_travel(body, elem_manager))

        elif condition.type == "list":
            raise NotImplementedError(f"[StmtTraveler] {type(condition.type)}는 지원하지 않는 타입입니다.")
        else:
            raise TypeError(f"[StmtTraveler] {type(condition.type)}는 잘못된 타입입니다.")

        return for_stmt_obj

    @staticmethod
    def expr_travel(node: ast.Expr, elem_manager: CodeElementManager):
        return ExprStmt.parse(node.value, elem_manager)

    @staticmethod
    def _internal_travel(node: ast, elem_manager: CodeElementManager):
        if isinstance(node, ast.For):
            return StmtTraveler.for_travel(node, elem_manager)

        elif isinstance(node, ast.Expr):
            return StmtTraveler.expr_travel(node, elem_manager)

        else:
            raise TypeError(f"[StmtTraveler] {type(node)}는 잘못된 타입입니다.")
