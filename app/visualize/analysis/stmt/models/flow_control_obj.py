from dataclasses import dataclass, field
from typing import Any

from app.visualize.analysis.stmt.models.stmt_type import StmtType


@dataclass(frozen=True)
class BreakStmtObj:
    id: int
    flow_control_type: StmtType = field(default_factory=lambda: StmtType.BREAK, init=False)
    type: StmtType = field(default_factory=lambda: StmtType.FLOW_CONTROL, init=False)


@dataclass(frozen=True)
class PassStmtObj:
    id: int
    flow_control_type: StmtType = field(default_factory=lambda: StmtType.PASS, init=False)
    type: StmtType = field(default_factory=lambda: StmtType.FLOW_CONTROL, init=False)


@dataclass(frozen=True)
class ContinueStmtObj:
    id: int
    flow_control_type: StmtType = field(default_factory=lambda: StmtType.CONTINUE, init=False)
    type: StmtType = field(default_factory=lambda: StmtType.FLOW_CONTROL, init=False)


@dataclass(frozen=True)
class ReturnStmtObj:
    id: int
    value: Any
    expr: tuple[str, ...]
    flow_control_type: StmtType = field(default_factory=lambda: StmtType.RETURN, init=False)
    type: StmtType = field(default_factory=lambda: StmtType.FLOW_CONTROL, init=False)
