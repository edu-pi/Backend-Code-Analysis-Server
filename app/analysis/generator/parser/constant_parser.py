import ast
from dataclasses import dataclass


class ConstantParser:

    def __init__(self, node):
        self.__value = node.value

    @staticmethod
    def parse(node):
        constant_parser = ConstantParser(node)

        return Constant(
            value=constant_parser.__get_value(),
            expressions=constant_parser.__get_expressions()
        )

    def __get_value(self):
        return self.__value

    def __get_expressions(self):
        return [str(self.__value)]


@dataclass
class Constant:
    value: int
    expressions: list
