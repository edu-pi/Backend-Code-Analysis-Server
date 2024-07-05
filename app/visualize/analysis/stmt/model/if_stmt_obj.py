from dataclasses import dataclass

from app.visualize.analysis.stmt.expr.model.expr_obj import ExprObj
from app.visualize.analysis.stmt.model.for_stmt_obj import BodyObj


@dataclass(frozen=True)
class ConditionObj:
    id: int
    expr_obj: ExprObj | None
    result: bool


@dataclass(frozen=True)
class IfConditionObj(ConditionObj):
    pass


@dataclass(frozen=True)
class ElifConditionObj(ConditionObj):
    pass


@dataclass(frozen=True)
class ElseConditionObj(ConditionObj):
    pass


@dataclass(frozen=True)
class IfStmtObj:
    conditions: tuple[ConditionObj, ...]  # 조건문들의 정보
    body: BodyObj  # 조건문이 true인 If문에서 실행되는 body 로직 정보
    type: str = "if"
