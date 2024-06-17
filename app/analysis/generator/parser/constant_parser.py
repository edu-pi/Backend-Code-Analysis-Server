import ast
from dataclasses import dataclass


class ConstantParser:

    @staticmethod
    def parse(node):
        return Constant(
            value=ConstantParser.__get_value(node),
            expressions=ConstantParser.__get_expressions(node)
        )

    @staticmethod
    def __get_value(node):
        return node.value

    @staticmethod
    def __get_expressions(node):
        return [str(node.value)]


@dataclass
class Constant:
    value: int
    expressions: list
