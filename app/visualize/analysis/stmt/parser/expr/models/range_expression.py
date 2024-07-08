from dataclasses import dataclass


@dataclass(frozen=True)
class RangeExpression:
    start: str
    end: str
    step: str
