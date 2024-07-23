from dataclasses import dataclass, field
from typing import Any

from app.visualize.analysis.stmt.models.stmt_type import StmtType
from app.visualize.analysis.stmt.parser.expr.models.expr_obj import ExprObj


@dataclass
class BodyObj:
    cur_value: Any
    body_steps: list[Any]


@dataclass
class ForStmtObj:
    id: int
    target_name: str
    iter_obj: ExprObj
    body_objs: list[BodyObj] = None
    type: StmtType = field(default_factory=lambda: StmtType.FOR, init=False)
