import ast

from app.analysis.parser import assign_parse, for_parse


def print_ast(node, level=0):
    print(ast.dump(node, indent=2))


def visualize_code(parsed_ast):
    for node in parsed_ast.body:
        parse_node(node)


def parse_node(node, target_name=None):
    if isinstance(node, ast.Assign):
        assign_parse(node)
    elif isinstance(node, ast.For):
        for_parse(node)

