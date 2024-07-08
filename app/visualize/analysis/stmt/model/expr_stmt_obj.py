from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class ExprStmtObj:
    id: int
    value: Any
    expressions: tuple[str]
    type: str = "expr"
