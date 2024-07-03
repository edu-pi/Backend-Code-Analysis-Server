from dataclasses import dataclass


@dataclass
class AssignStmtObj:
    id: int
    targets: list[str]
    value: str
    expressions: list[str]
    var_type: str
    type: str = "assign"
