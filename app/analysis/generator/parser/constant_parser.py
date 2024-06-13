import ast
from dataclasses import dataclass


class ConstantParser:

    def __init__(self, node: ast.Constant):
        self.node = node

    def parse(self):
        return Constant(self.node.value)


@dataclass
class Constant:
    value: int
