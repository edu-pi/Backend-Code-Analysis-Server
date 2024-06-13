import ast


class Constant:

    def __init__(self, node: ast.Constant):
        self.node = node

    def get_value(self):
        return self.node.value
