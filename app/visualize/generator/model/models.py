from dataclasses import dataclass


@dataclass(frozen=True)
class AssignViz:
    variables: list
    type: str = "assignViz"


'''
    @ list: Variable 리스트
    @ type: 타입
'''


@dataclass(frozen=True)
class Variable:
    depth: int
    expr: str
    name: str


'''
    @ depth: 깊이
    @ expr: 변수에 들어갈 표현식
    @ name: 변수 이름
'''


@dataclass
class ConditionViz:
    target: str
    cur: int
    start: int
    end: int
    step: int

    def copy_with_new_cur(self, new_cur):
        return ConditionViz(self.target, new_cur, self.start, self.end, self.step)

    def changed_attr(self):
        if self.start == self.cur:
            return list(self.__dict__.keys())

        return ['cur']


@dataclass(frozen=True)
class ForViz:
    id: int
    depth: int
    condition: ConditionViz
    highlight: []
    type: str = "for"


'''
    @ id: 식별값
    @ depth: 깊이
    @ condition: 조건절
    @ type : 타입
'''


@dataclass(frozen=True)
class PrintViz:
    id: int
    depth: int
    expr: str
    highlight: []
    console: str
    type: str = "print"


'''
    @ id: 식별값
    @ depth: 깊이
    @ name: 변수 이름
    @ value: 변수 값

'''
