from dataclasses import dataclass


@dataclass
class AssignObj:
    targets: list[str]
    value: str
    type: str = "assign"


@dataclass
class AssignStmtObj:
    assign_steps: list[AssignObj]
    type: str = "assign_list"
