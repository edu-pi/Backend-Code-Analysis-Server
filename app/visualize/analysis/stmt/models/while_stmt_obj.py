from dataclasses import dataclass, field

from app.visualize.analysis.stmt.models.stmt_type import StmtType


@dataclass
class WhileStep:
    condition_expr: tuple[str, ...]
    body_steps: list


@dataclass(frozen=True)
class WhileStmtObj:
    id: int
    while_steps: list[WhileStep]
    orelse_steps: list
    orelse_id: int | None
    type: StmtType = field(default_factory=lambda: StmtType.WHILE, init=False)
