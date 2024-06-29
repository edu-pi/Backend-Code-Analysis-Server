from dataclasses import dataclass


@dataclass(frozen=True)
class RangeExpression:
    start: str
    end: str
    step: str


@dataclass(frozen=True)
class RangeExprObj:
    expressions: tuple[RangeExpression]
    iterator: tuple
    type: str = "range"
