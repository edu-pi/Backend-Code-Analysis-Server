import ast
from dataclasses import dataclass


class ConstantParser:

    def __init__(self, node: ast.Constant):
        self.node = node

    def parse(self):
        return Constant(value=self.__get_value(), expressions=self.__get_expressions())

    def __get_value(self):
        return self.node.value

    def __get_expressions(self):
        return [self.node.value]


@dataclass
class Constant:
    value: int
    expressions: list
