from dataclasses import dataclass


@dataclass
class AssignStmtObj:
    targets: list[str]
    value: str
    expressions: list[str]
    type: str = "assign"
