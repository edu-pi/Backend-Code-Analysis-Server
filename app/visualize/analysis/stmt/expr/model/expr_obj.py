from dataclasses import dataclass, field
from typing import Any

from app.visualize.analysis.stmt.expr.model.range_expression import RangeExpression


@dataclass(frozen=True)
class ExprObj:
    type: str
    value: Any
    expressions: tuple[Any, ...]


@dataclass(frozen=True)
class PrintObj(ExprObj):
    value: str
    expressions: tuple[str, ...]
    type: str = field(default="print", init=False)


@dataclass(frozen=True)
class BinopObj(ExprObj):
    value: Any
    expressions: tuple[str, ...]
    type: str = field(default="binop", init=False)


@dataclass(frozen=True)
class CallObj(ExprObj):
    value: Any
    expressions: tuple[str, ...]
    type: str = field(default="call", init=False)


@dataclass(frozen=True)
class ConstantObj(ExprObj):
    value: Any
    expressions: tuple[str, ...]
    type: str = field(default="constant", init=False)


@dataclass(frozen=True)
class NameObj(ExprObj):
    value: Any
    expressions: tuple[str, ...]
    type: str = field(default="name", init=False)


@dataclass(frozen=True)
class ListObj(ExprObj):
    value: tuple
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
    expressions: tuple[str, ...]
    type: str = field(default="print", init=False)
