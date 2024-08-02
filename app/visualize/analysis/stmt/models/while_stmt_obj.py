from dataclasses import dataclass, field

from app.visualize.analysis.stmt.models.stmt_type import StmtType


@dataclass
class WhileCycle:
    condition_exprs: tuple[str, ...]
    body_objs: list


@dataclass(frozen=True)
class WhileStmtObj:
    id: int
    while_cycles: list[WhileCycle]
    type: StmtType = field(default_factory=lambda: StmtType.WHILE, init=False)
