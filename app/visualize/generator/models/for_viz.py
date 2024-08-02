from dataclasses import dataclass, field


@dataclass(frozen=True)
class ForConditionViz:
    target: str
    cur: str
    start: str
    end: str
    step: str

    def copy_with_cur(self, new_cur: str):
        return ForConditionViz(self.target, str(new_cur), self.start, self.end, self.step)

    def changed_attr(self):
        if str(self.cur) == self.start:
            return list(self.__dict__.keys())

        return ["cur"]


@dataclass(frozen=True)
class ForViz:
    id: int
    depth: int
    condition: ForConditionViz
    highlights: []
    type: str = field(default="for", init=False)

    def update(self, new_condition, highlights):
        return ForViz(self.id, self.depth, new_condition, highlights)


"""
    @ id: 식별값
    @ depth: 깊이
    @ condition: 조건절
    @ type : 타입
"""
