from dataclasses import dataclass
from typing import Any


@dataclass
class AssignStmtObj:
    id: int
    targets: list[str]
    value: Any
    expressions: list[str]
    var_type: str
    type: str = "assign"
