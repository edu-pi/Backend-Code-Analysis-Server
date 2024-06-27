from dataclasses import dataclass
from typing import Any


@dataclass
class ExprStmtObj:
    type: str
    value: Any
    expressions: list[str]
