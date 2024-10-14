from dataclasses import dataclass, field

from app.visualize.analysis.stmt.parser.expr.models.expr_type import ExprType


@dataclass
class Argument:
    expr: str
    name: str
    type: ExprType


@dataclass(frozen=True)
class CallUserFuncViz:
    id: int
    assignName: str
    depth: int
    signature: str
    code: str
    type: str = field(default="callUserFunc", init=False)


@dataclass(frozen=True)
class CreateCallStackViz:
    args: list[Argument]
    callStackName: str
    code: str
    type: str = field(default="createCallStack", init=False)


@dataclass(frozen=True)
class EndUserFuncViz:
    id: int
    returnValue: str
    depth: int
    type: str = field(default="endUserFunc", init=False)
