from dataclasses import dataclass, field
from typing import Any

from app.visualize.analysis.stmt.parser.expr.models.range_expression import RangeExpression


@dataclass(frozen=True)
class ExprObj:
    value: Any
    expressions: tuple[str, ...]
    type: str


@dataclass(frozen=True)
class BinopObj(ExprObj):
    type: str = field(default="binop", init=False)


@dataclass(frozen=True)
class CompareObj(ExprObj):
    type: str = field(default="compare", init=False)


@dataclass(frozen=True)
class CallObj(ExprObj):
    type: str = field(default="call", init=False)


@dataclass(frozen=True)
class ConstantObj(ExprObj):
    type: str = field(default="constant", init=False)


@dataclass(frozen=True)
class NameObj(ExprObj):
    type: str = field(default="name", init=False)


@dataclass(frozen=True)
class ListObj(ExprObj):
    value: list
    expressions: tuple[str, ...]
    type: str = field(default="list", init=False)


@dataclass(frozen=True)
class RangeObj(ExprObj):
    expressions: tuple[RangeExpression, ...]
    value: tuple
    type: str = field(default="range", init=False)


@dataclass(frozen=True)
class PrintObj(ExprObj):
    value: str
    type: str = field(default="print", init=False)
