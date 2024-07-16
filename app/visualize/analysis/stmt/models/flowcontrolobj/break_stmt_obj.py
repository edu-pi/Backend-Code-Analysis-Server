from dataclasses import dataclass, field


@dataclass(frozen=True)
class BreakStmtObj:
    id: int
    expr: str
    type: str = field(default="flowControl", init=False)
