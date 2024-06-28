from dataclasses import dataclass


@dataclass
class PrintExprObj:
    value: str
    expressions: list[str]
    type: str = "print"
