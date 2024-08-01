from dataclasses import dataclass, field

from app.visualize.analysis.stmt.parser.expr.models.expr_type import ExprType


@dataclass(frozen=True)
class ExprViz:
    id: int
    depth: int
    expr: ExprType
    type: str
