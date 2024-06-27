from dataclasses import dataclass

from app.visualize.analysis.stmt.expr.model.expr_obj import ExprObj


@dataclass
class ForStmtObj:
    init_value: ExprObj
    condition: ExprObj
    type: str = "for"
