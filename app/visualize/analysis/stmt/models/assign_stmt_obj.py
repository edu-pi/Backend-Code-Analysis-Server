from dataclasses import dataclass, field

from app.visualize.analysis.stmt.models.expr_stmt_obj import ExprStmtObj
from app.visualize.analysis.stmt.models.stmt_type import StmtType


@dataclass(frozen=True)
class AssignStmtObj:
    targets: tuple[str, ...]
    expr_stmt_obj: ExprStmtObj
    call_stack_name: str
    type: StmtType = field(default_factory=lambda: StmtType.ASSIGN, init=False)
