from dataclasses import dataclass

from app.visualize.analysis.stmt.model.for_stmt_obj import BodyObj


@dataclass(frozen=True)
class ConditionObj:
    id: int
    expressions: tuple[str, ...] | None  # else의 경우 None
    result: bool


class IfConditionObj(ConditionObj):
    pass


class ElifConditionObj(ConditionObj):
    pass


class ElseConditionObj(ConditionObj):
    pass


@dataclass(frozen=True)
class IfStmtObj:
    conditions: tuple[ConditionObj, ...]  # 조건문들의 정보
    body: BodyObj  # 조건문이 true인 If문에서 실행되는 body 로직 정보
    type: str = "if"
