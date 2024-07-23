from dataclasses import dataclass, field
from typing import Any

from app.visualize.analysis.stmt.models.for_stmt_obj import BodyObj
from app.visualize.analysis.stmt.models.stmt_type import StmtType


@dataclass(frozen=True)
class ConditionObj:
    id: int
    expressions: tuple[str, ...] | None  # else의 경우 None
    result: bool
    type: StmtType


@dataclass(frozen=True)
class IfConditionObj(ConditionObj):
    type: StmtType = field(default_factory=lambda: StmtType.IF, init=False)


@dataclass(frozen=True)
class ElifConditionObj(ConditionObj):
    type: StmtType = field(default_factory=lambda: StmtType.ELIF, init=False)


@dataclass(frozen=True)
class ElseConditionObj(ConditionObj):
    type: StmtType = field(default_factory=lambda: StmtType.ELSE, init=False)


@dataclass(frozen=True)
class IfStmtObj:
    conditions: tuple[ConditionObj, ...]  # 조건문들의 정보
    body_steps: list  # 조건문이 true인 If문에서 실행되는 body 로직 정보
    type: StmtType = field(default_factory=lambda: StmtType.IF, init=False)

    def create_with_new_body(self, new_body_steps):
        return IfStmtObj(conditions=self.conditions, body_steps=new_body_steps)
