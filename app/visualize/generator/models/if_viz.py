from dataclasses import dataclass


@dataclass(frozen=True)
class ConditionViz:
    id: int
    expr: str
    type: str


@dataclass(frozen=True)
class IfElseDefineViz:
    depth: int
    conditions: tuple[ConditionViz, ...]
    type: str = "ifElseDefine"


@dataclass(frozen=True)
class IfElseChangeViz:
    id: int
    depth: int
    expr: str
    type: str = "ifElseChange"
