import ast

from app.analysis.parser import assign_parse, for_parse


def print_ast(node, level=0):
    print('  ' * level + ast.dump(node))
    for child in ast.iter_child_nodes(node):
        print_ast(child, level + 1)


def visualize_code(parsed_ast):
    for node in parsed_ast.body:
        parse_node(node)


def parse_node(node, target_name=None):
    if isinstance(node, ast.Assign):
        assign_parse(node)
    elif isinstance(node, ast.For):
        for_parse(node)

