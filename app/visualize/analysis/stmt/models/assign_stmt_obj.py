from dataclasses import dataclass, field

from app.visualize.analysis.stmt.models.expr_stmt_obj import ExprStmtObj
from app.visualize.analysis.stmt.models.stmt_type import StmtType
from app.visualize.analysis.stmt.models.user_func_stmt_obj import UserFuncStmtObj


@dataclass(frozen=True)
class AssignStmtObj:
    targets: tuple[str, ...]
    expr_stmt_obj: ExprStmtObj | UserFuncStmtObj
    call_stack_name: str
    type: StmtType = field(default_factory=lambda: StmtType.ASSIGN, init=False)
