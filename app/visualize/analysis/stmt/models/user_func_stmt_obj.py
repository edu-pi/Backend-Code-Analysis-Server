from dataclasses import dataclass, field
from typing import Any

from app.visualize.analysis.stmt.models.stmt_type import StmtType


@dataclass(frozen=True)
class UserFuncStmtObj:
    id: int
    func_id: int
    func_name: str
    func_signature: str
    body_steps: list[Any]
    args: dict
    value: Any
    expr: tuple
    return_argument_name: str
    type: StmtType = field(default_factory=lambda: StmtType.USER_FUNC, init=False)
