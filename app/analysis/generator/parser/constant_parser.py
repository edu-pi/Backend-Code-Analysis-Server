import ast
from dataclasses import dataclass


class ConstantParser:

    def __init__(self, node: ast.Constant):
        self.value = node.value

    def parse(self):
        return Constant(value=self.__get_value(), expressions=self.__get_expressions())

    def __get_value(self):
        return self.value

    def __get_expressions(self):
        return [str(self.value)]


@dataclass
class Constant:
    value: int
    expressions: list
