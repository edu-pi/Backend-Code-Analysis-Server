from dataclasses import dataclass, field


@dataclass(frozen=True)
class SubscriptIdx:
    start: int
    end: int


@dataclass(frozen=True)
class Variable:
    id: int
    expr: str
    name: str
    code: str
    type: str
    idx: SubscriptIdx = field(default=SubscriptIdx(0, 0))
