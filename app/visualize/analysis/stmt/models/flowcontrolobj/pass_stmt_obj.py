from dataclasses import dataclass, field


@dataclass(frozen=True)
class PassStmtObj:
    id: int
    expr: str
    type: str = field(default="flowControl", init=False)