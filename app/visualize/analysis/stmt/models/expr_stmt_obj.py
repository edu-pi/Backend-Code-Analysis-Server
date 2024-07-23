from dataclasses import dataclass, field
from typing import Any

from app.visualize.analysis.stmt.models.stmt_type import StmtType
from app.visualize.analysis.stmt.parser.expr.models.expr_type import ExprType


@dataclass(frozen=True)
class ExprStmtObj:
    id: int
    value: Any
    expressions: tuple[str]
    expr_type: ExprType
    type: StmtType = field(default_factory=lambda: StmtType.EXPR, init=False)
