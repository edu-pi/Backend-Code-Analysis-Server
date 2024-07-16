from dataclasses import dataclass


@dataclass(frozen=True)
class ExprViz:
    id: int
    depth: int
    expr: str
    type: str
