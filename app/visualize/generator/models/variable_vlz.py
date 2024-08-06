from dataclasses import dataclass


@dataclass(frozen=True)
class Variable:
    id: int
    expr: str
    name: str
    code: str
    type: str
