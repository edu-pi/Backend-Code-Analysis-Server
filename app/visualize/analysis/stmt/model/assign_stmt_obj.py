from dataclasses import dataclass


@dataclass
class AssignStmtObj:
    id: int
    targets: list[str]
    value: str
    expressions: list[str]
    type: str = "assign"
