from dataclasses import dataclass, field
from typing import Any

from app.visualize.analysis.stmt.parser.expr.models.expr_type import ExprType
from app.visualize.analysis.stmt.parser.expr.models.range_expression import RangeExpression
from app.visualize.analysis.stmt.parser.expr.models.slice_expression import SliceExpression


@dataclass(frozen=True)
class ExprObj:
    value: Any
    expressions: tuple
    type: ExprType


@dataclass(frozen=True)
class BinopObj(ExprObj):
    expressions: tuple[str, ...]
    type: ExprType = field(default=ExprType.VARIABLE, init=False)


@dataclass(frozen=True)
class CompareObj(ExprObj):
    expressions: tuple[str, ...]
    type: ExprType = field(default=ExprType.COMPARE, init=False)


@dataclass(frozen=True)
class ConstantObj(ExprObj):
    expressions: tuple[str, ...]
    type: ExprType = field(default=ExprType.VARIABLE, init=False)


@dataclass(frozen=True)
class NameObj(ExprObj):
    expressions: tuple[str, ...]
    type: ExprType


@dataclass(frozen=True)
class ListObj(ExprObj):
    value: list
    expressions: tuple[str, ...]
    type: ExprType = field(default=ExprType.LIST, init=False)


@dataclass(frozen=True)
class TupleObj(ExprObj):
    value: tuple
    expressions = tuple[str, ...]
    type: ExprType = field(default=ExprType.TUPLE, init=False)


@dataclass(frozen=True)
class DictObj(ExprObj):
    value: dict
    expressions = tuple[str, ...]
    type: ExprType = field(default=ExprType.DICT, init=False)


@dataclass(frozen=True)
class CallObj(ExprObj):
    expressions: tuple[str, ...]
    type: ExprType = field(default=ExprType.CALL, init=False)


@dataclass(frozen=True)
class RangeObj(CallObj):
    value: tuple
    expressions: tuple[RangeExpression, ...]
    type: ExprType = field(default=ExprType.RANGE, init=False)


@dataclass(frozen=True)
class PrintObj(CallObj):
    value: str
    type: ExprType = field(default=ExprType.PRINT, init=False)


@dataclass(frozen=True)
class InputObj(CallObj):
    value: str
    expressions: tuple[str, ...]
    type: ExprType = field(default=ExprType.INPUT, init=False)


@dataclass(frozen=True)
class SubscriptObj(ExprObj):
    expressions = tuple[str, ...]
    type: ExprType


@dataclass(frozen=True)
class SliceObj(ExprObj):
    value: slice
    expressions = tuple[SliceExpression, ...]
    type: ExprType = field(default=ExprType.SLICE, init=False)


@dataclass(frozen=True)
class AttributeObj(ExprObj):
    expressions: tuple[str, ...]
    type: ExprType


@dataclass(frozen=True)
class AppendObj(AttributeObj):
    value: str
    expressions: tuple[str, ...]
    type: ExprType = field(default=ExprType.APPEND, init=False)


@dataclass(frozen=True)
class RemoveObj(AttributeObj):
    value: str
    expressions: tuple[str, ...]
    type: ExprType = field(default=ExprType.REMOVE, init=False)


@dataclass(frozen=True)
class ExtendObj(AttributeObj):
    value: str
    expressions: tuple[str, ...]
    type: ExprType = field(default=ExprType.EXTEND, init=False)


@dataclass(frozen=True)
class PopObj(AttributeObj):
    value: str
    expressions: tuple[str, ...]
    type: ExprType = field(default=ExprType.POP, init=False)


@dataclass(frozen=True)
class InsertObj(AttributeObj):
    value: str
    expressions: tuple[str, ...]
    type: ExprType = field(default=ExprType.INSERT, init=False)


@dataclass(frozen=True)
class FormattedValueObj(ExprObj):
    value: str
    expressions: tuple[str, ...]
    type: ExprType = field(default=ExprType.VARIABLE, init=False)


@dataclass(frozen=True)
class ArgumentsObj(ExprObj):
    value: tuple[str, ...]
    expressions: tuple[str, ...]
    type: ExprType = field(default=ExprType.VARIABLE, init=False)
