from dataclasses import dataclass


@dataclass(frozen=True)
class Variable:
    depth: int
    target: str
    expr: str
    type: str = "variable"


'''
    @ id: 식별값
    @ depth: 깊이
    @ name: 변수 이름
    @ value: 변수 값

'''


@dataclass
class Condition:
    target: str
    cur: int
    start: int
    end: int
    step: int

    def copy_with_new_cur(self, new_cur):
        return Condition(self.target, self.start, self.end, self.step, new_cur)

    def changed_attr(self, new_condition):
        if new_condition is None:
            return list(self.__dict__.keys())

        changed_attributes = []
        attributes = ['cur', 'start', 'end']

        for attr in attributes:
            if getattr(self, attr) != getattr(new_condition, attr):
                changed_attributes.append(attr)

        return changed_attributes


@dataclass(frozen=True)
class For:
    id: int
    depth: int
    condition: Condition
    highlight: []
    type: str = "for"


'''
    @ id: 식별값
    @ depth: 깊이
    @ condition: 조건절
    @ type : 타입
'''


@dataclass(frozen=True)
class Print:
    id: int
    depth: int
    expr: str
    type: str = "print"


'''
    @ id: 식별값
    @ depth: 깊이
    @ name: 변수 이름
    @ value: 변수 값

'''