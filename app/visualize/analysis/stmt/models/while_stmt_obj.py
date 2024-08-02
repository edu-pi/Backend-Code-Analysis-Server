from dataclasses import dataclass, field

from app.visualize.analysis.stmt.models.stmt_type import StmtType


@dataclass
class WhileStep:
    condition_exprs: tuple[str, ...]
    body_steps: list


@dataclass(frozen=True)
class WhileStmtObj:
    id: int
    while_steps: list[WhileStep]
    type: StmtType = field(default_factory=lambda: StmtType.WHILE, init=False)
