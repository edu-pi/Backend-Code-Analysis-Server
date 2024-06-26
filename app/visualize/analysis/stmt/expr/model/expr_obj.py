from dataclasses import dataclass
from typing import Any


@dataclass
class ExprObj:
    type: str
    value: Any
    expressions: list[Any]
