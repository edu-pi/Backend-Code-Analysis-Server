from copy import deepcopy
from dataclasses import dataclass


@dataclass(frozen=True)
class AssignViz:
    variables: list
    type: str = "assignViz"


"""
    @ list: Variable 리스트
    @ type: 타입````
"""


@dataclass(frozen=True)
class Variable:
    depth: int
    expr: str
    name: str
    highlights: list


"""
    @ depth: 깊이
    @ expr: 변수에 들어갈 표현식
    @ name: 변수 이름
"""


@dataclass(frozen=True)
class ConditionViz:
    target: str
    cur: int
    start: int
    end: int
    step: int

    def copy_with_cur(self, new_cur):
        return ConditionViz(self.target, new_cur, self.start, self.end, self.step)

    def changed_attr(self):
        if str(self.cur) == self.start:
            return list(self.__dict__.keys())

        return ["cur"]


@dataclass(frozen=True)
class ForViz:
    id: int
    depth: int
    condition: ConditionViz
    highlights: []
    type: str = "for"

    def update(self, new_condition, highlights):
        return ForViz(self.id, self.depth, new_condition, highlights)


"""
    @ id: 식별값
    @ depth: 깊이
    @ condition: 조건절
    @ type : 타입
"""


@dataclass(frozen=True)
class PrintViz:
    id: int
    depth: int
    expr: str
    highlight: []
    console: str
    type: str = "print"


"""
    @ id: 식별값
    @ depth: 깊이
    @ name: 변수 이름
    @ value: 변수 값

"""
