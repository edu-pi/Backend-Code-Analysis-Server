import ast
from dataclasses import dataclass

from app.analysis.element_manager import CodeElementManager


class NameParser:

    def __init__(self, node: ast.Name, elem_manager: CodeElementManager):
        self.ctx = node.ctx
        self.id = node.id
        self.elem_manager = elem_manager

    def parse(self):
        value = self.__get_value()
        expressions = self.__get_expressions(value)
        return Name(self.id, value, expressions)

    # 변수의 값을 가져오는 함수
    def __get_value(self):
        try:
            return self.elem_manager.get_variable_value(name=self.id)
        except NameError as e:
            print("#error:", e)

    # 변수의 변화 과정을 만들어주는 함수
    def __get_expressions(self, value):
        return [self.id, value]


@dataclass
class Name:
    id: str
    value: int
    expressions: list
