from dataclasses import dataclass
from typing import Any

from app.visualize.analysis.stmt.expr.model.expr_obj import RangeObj


@dataclass
class BodyObj:
    cur_value: Any
    body_steps: list[Any]


@dataclass
class ForStmtObj:
    id: int
    target_name: str
    iter_obj: RangeObj
    body_objs: list[BodyObj] = None
    type: str = "for"
