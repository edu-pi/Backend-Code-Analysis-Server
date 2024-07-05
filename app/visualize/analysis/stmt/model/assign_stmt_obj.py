from dataclasses import dataclass
from typing import Any

from app.visualize.analysis.stmt.model.expr_stmt_obj import ExprStmtObj


@dataclass(frozen=True)
class AssignStmtObj:
    targets: tuple[str, ...]
    expr_stmt_obj: ExprStmtObj
    type: str = "assign"
