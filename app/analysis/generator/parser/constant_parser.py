import ast
from dataclasses import dataclass


class ConstantParser:

    def __init__(self, node: ast.Constant):
        self.__value = node.value

    def parse(self):
        return Constant(value=self.__get_value(), expressions=self.__get_expressions())

    def __get_value(self):
        return self.__value

    def __get_expressions(self):
        return [str(self.__value)]


@dataclass
class Constant:
    value: int
    expressions: list
