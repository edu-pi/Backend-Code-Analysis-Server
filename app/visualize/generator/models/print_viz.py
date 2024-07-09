from dataclasses import dataclass


@dataclass(frozen=True)
class PrintViz:
    id: int
    depth: int
    expr: str
    highlights: []
    console: str | None
    type: str = "print"


"""
    @ id: 식별값
    @ depth: 깊이
    @ name: 변수 이름
    @ value: 변수 값

"""
