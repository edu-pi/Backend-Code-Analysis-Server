from dataclasses import dataclass


@dataclass(frozen=True)
class Variable:
    depth: int
    name: str
    expr: str
    type: str = "variable"


'''
    @ id: 식별값
    @ depth: 깊이
    @ name: 변수 이름
    @ value: 변수 값

'''


@dataclass(frozen=True)
class Condition:
    name: str
    start: str
    end: str
    step: str
    cur: str

    def copy_with_new_cur(self, new_cur):
        return Condition(self.name, self.start, self.end, self.step, new_cur)


@dataclass(frozen=True)
class For:
    id: int
    depth: int
    condition: Condition
    type: str = "for"


'''
    @ id: 식별값
    @ depth: 깊이
    @ condition: 조건절
    @ type : 타입
'''
