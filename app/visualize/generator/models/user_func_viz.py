from dataclasses import dataclass, field

from app.visualize.analysis.stmt.parser.expr.models.expr_type import ExprType
from app.visualize.generator.models.variable_vlz import SubscriptIdx


@dataclass
class Argument:
    id: int
    expr: str
    name: str
    code: str
    type: ExprType
    idx: SubscriptIdx = field(default=SubscriptIdx(0, 0))


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
    id: int
    args: list[Argument]
    callStackName: str
    code: str
    type: str = field(default="createCallStack", init=False)


@dataclass(frozen=True)
class EndUserFuncViz:
    id: int
    depth: int
    returnExpr: str
    returnName: str
    code: str
    delFuncName: str
    type: str = field(default="endUserFunc", init=False)
