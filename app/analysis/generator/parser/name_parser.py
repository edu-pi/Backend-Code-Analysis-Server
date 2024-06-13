import ast

from app.analysis.element_manager import CodeElementManager


class Name:

    def __init__(self, node: ast.Name, elem_manager: CodeElementManager):
        self.elem_manager = elem_manager
        self.node = node

    # 변수의 값을 가져오는 함수
    def get_value(self):
        try:
            return self.elem_manager.get_variable_value(name=self.node.id)
        except NameError as e:
            print("#error:", e)

    # 변수의 변화 과정을 만들어주는 함수
    def get_expressions(self):
        return [self.node.id, self.get_value()]
