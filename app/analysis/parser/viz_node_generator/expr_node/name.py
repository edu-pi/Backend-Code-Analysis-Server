import ast

from app.analysis.element_manager import CodeElementManager


class Name:

    def __init__(self, node: ast.Name, elem_manager: CodeElementManager):
        self.elem_manager = elem_manager
        self.node = node

    def get_value(self):
        try:
            return self.elem_manager.get_variable_value(name=self.node.id)
        except NameError as e:
            print("#error:", e)

    def get_expression(self):
        return [self.node.id, self.get_value()]
