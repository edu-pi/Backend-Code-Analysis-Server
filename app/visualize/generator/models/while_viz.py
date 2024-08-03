from dataclasses import dataclass


@dataclass
class WhileDefineViz:
    id: int
    expr: str
    depth: int
    type: str = "whileDefine"


@dataclass
class WhileChangeConditionViz:
    id: int
    depth: int
    expr: str
    type: str = "whileChangeCondition"
