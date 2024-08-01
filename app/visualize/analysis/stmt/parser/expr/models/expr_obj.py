from dataclasses import dataclass, field, replace
from typing import Any

from app.visualize.analysis.stmt.parser.expr.models.expr_type import ExprType
from app.visualize.analysis.stmt.parser.expr.models.range_expression import RangeExpression
from app.visualize.analysis.stmt.parser.expr.models.slice_expression import SliceExpression


@dataclass(frozen=True)
class ExprObj:
    value: Any
    expressions: tuple
    type: ExprType

    def add_bool_if_not_condition(self):
        if self.expressions[-1] in ("True", "False"):
            return self

        condition = "True" if self.value else "False"
        return replace(self, expressions=self.expressions + (condition,))


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
class SubscriptObj(ExprObj):
    expressions = tuple[str, ...]
    type: ExprType = field(default=ExprType.SUBSCRIPT, init=False)


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
