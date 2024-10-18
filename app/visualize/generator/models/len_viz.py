from dataclasses import dataclass, field


@dataclass(frozen=True)
class LenViz:
    id: int
    depth: int
    expr: str
    code: str
    type: str = field(default="len", init=False)
