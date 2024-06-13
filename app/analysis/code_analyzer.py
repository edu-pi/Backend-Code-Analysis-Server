import ast

from app.analysis.element_manager import CodeElementManager
from app.analysis.parser1 import assign_parse, for_parse
from app.analysis.step_manager import StepManager


class CodeAnalyzer:

    def __init__(self, elem_manager: CodeElementManager, step_manager: StepManager):
        self.elem_manager = elem_manager
        self.step_manager = step_manager

    @staticmethod
    def print_ast(node):
        print(ast.dump(node, indent=4))

    def visualize_code(self, parsed_ast):

        for node in parsed_ast.body:
            self.parse_node(node)
        return self.step_manager.get_viz_nodes()

    def parse_node(self, node):
        if isinstance(node, ast.Assign):
            steps = assign_parse(node, self.elem_manager)
            self.step_manager.add_steps(steps)

        elif isinstance(node, ast.For):
            for_parse(node, self.elem_manager)
