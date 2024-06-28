from dataclasses import dataclass


@dataclass
class RangeExpression:
    start: str
    end: str
    step: str


@dataclass
class RangeExprObj:
    expressions: list[RangeExpression]
    iterator: list
    type: str = "range"
