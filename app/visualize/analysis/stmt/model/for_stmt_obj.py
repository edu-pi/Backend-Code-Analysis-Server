from dataclasses import dataclass
from typing import Any

from app.visualize.analysis.stmt.expr.model.range_expr_obj import RangeExprObj


@dataclass
class BodyObj:
    cur_value: Any
    body_steps: list[Any]


@dataclass
class ForStmtObj:
    target_name: str
    iter_obj: RangeExprObj
    body_objs: list[BodyObj] = None
    type: str = "for"
