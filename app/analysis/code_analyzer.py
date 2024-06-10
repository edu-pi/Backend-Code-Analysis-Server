import ast

from app.analysis.element_manager import CodeElementManager
from app.analysis.parser import assign_parse, for_parse


class CodeAnalyzer:

    def __init__(self, elem_manager: CodeElementManager):
        self.elem_manager = elem_manager

    @staticmethod
    def print_ast(node):
        print(ast.dump(node, indent=4))

    def visualize_code(self, parsed_ast):
        for node in parsed_ast.body:
            self.parse_node(node)
        return self.elem_manager.get_all_step()

    def parse_node(self, node):
        if isinstance(node, ast.Assign):
            assign_parse(node, self.elem_manager)
        elif isinstance(node, ast.For):
            for_parse(node, self.elem_manager)
