from dataclasses import dataclass

from app.visualize.analysis.stmt.expr.model.expr_obj import ExprObj
from app.visualize.analysis.stmt.model.for_stmt_obj import BodyObj


@dataclass
class IfOrElifConditionObj:
    id: int
    expr_obj: ExprObj
    result: bool


@dataclass
class ElseConditionObj:
    id: int
    result: bool


@dataclass
class IfStmtObj:
    conditions: tuple[IfOrElifConditionObj | ElseConditionObj, ...]  # 조건문들의 정보
    body: BodyObj  # 조건문이 true인 If문에서 실행되는 body 로직 정보
    type: str = "if"
