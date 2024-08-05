from dataclasses import dataclass


@dataclass(frozen=True)
class Variable:
    id: int
    expr: str
    name: str
    code: str
    type: str


"""
    @ depth: 깊이
    @ expr: 변수에 들어갈 표현식
    @ name: 변수 이름
"""
