from dataclasses import dataclass
from typing import Any

from app.visualize.analysis.stmt.expr.model.range_expr_obj import RangeExprObj


@dataclass
class BodyStepObj:
    cur_value: Any
    body_objs: list[Any]


@dataclass
class ForStmtObj:
    target_name: str
    iter_obj: Any
    body_steps: list[BodyStepObj] = None
    type: str = "for"
