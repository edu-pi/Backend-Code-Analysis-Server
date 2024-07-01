from dataclasses import dataclass

from app.visualize.analysis.stmt.expr.model.expr_obj import ExprObj


@dataclass(frozen=True)
class ExprStmtObj:
    expr_obj: ExprObj
    type: str = "expr"
