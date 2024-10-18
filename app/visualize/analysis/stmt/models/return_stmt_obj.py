from dataclasses import dataclass, field
from typing import Any

from app.visualize.analysis.stmt.models.stmt_type import StmtType


@dataclass(frozen=True)
class ReturnStmtObj:
    id: int
    value: Any
    expr: tuple[str, ...]
    flow_control_type: StmtType = field(default_factory=lambda: StmtType.RETURN, init=False)
    type: StmtType = field(default_factory=lambda: StmtType.RETURN, init=False)
