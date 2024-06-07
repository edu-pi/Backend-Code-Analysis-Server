import ast

from app.analysis.parser import assign_parse, for_parse


class CodeAnalyzer:

    @staticmethod
    def print_ast(node):
        print(ast.dump(node, indent=4))

    def visualize_code(self, parsed_ast, g_elem_manager):
        for node in parsed_ast.body:
            self.parse_node(node, g_elem_manager)

    @staticmethod
    def parse_node(node, g_elem_manager, target_name=None):
        if isinstance(node, ast.Assign):
            assign_parse(node, g_elem_manager)
        elif isinstance(node, ast.For):
            for_parse(node, g_elem_manager)
