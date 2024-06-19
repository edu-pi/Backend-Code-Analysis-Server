import ast

from app.analysis.models import AssignViz, Variable

"""
case1: a = 1
case2: a, b = 1, 2
case3: a = b = 1 + 2
"""

targets = [
    [  # a
        ast.Name(id="a", ctx=ast.Store())
    ],
    [  # (a, b)
        ast.Tuple(elts=[
            ast.Name(id="a", ctx=ast.Store()),
            ast.Name(id="b", ctx=ast.Store())
        ], ctx=ast.Store())
    ],
    [  # a = b
        ast.Name(id="a", ctx=ast.Store()),
        ast.Name(id="b", ctx=ast.Store())
    ]
]

value = [
    ast.Constant(value=1),
    ast.Tuple(elts=[
        ast.Constant(value=1),
        ast.Constant(value=2)
    ], ctx=ast.Load()),
    ast.BinOp(left=ast.Constant(value=1), op=ast.Add(), right=ast.Constant(value=2))
]

parsed_targets = [
    ["a"],
    [("a", "b")],
    ["a", "b"]
]

parsed_values = [1, (1, 2), 3]

parsed_expressions = [
    ["1"],
    [('1', '2')],
    ["1 + 2", "3"]
]

saved_variables = [
    {"a": 1},
    {"a": 1, "b": 2},
    {"a": 3, "b": 3}
]

expected_viz = [
    [
        AssignViz(
            variables=[
                Variable(depth=1, expr="1", name="a")
            ]
        )
    ],
    [
        AssignViz(
            variables=[
                Variable(depth=1, expr="1", name="a"),
                Variable(depth=1, expr="2", name="b")
            ]
        )
    ],
    [
        AssignViz(
            variables=[
                Variable(depth=1, expr="1 + 2", name="a"),
                Variable(depth=1, expr="1 + 2", name="b")
            ]
        ),
        AssignViz(
            variables=[
                Variable(depth=1, expr="3", name="a"),
                Variable(depth=1, expr="3", name="b")
            ]
        )
    ]
]


def create_param():
    return list(zip(
        targets,
        value,
        parsed_targets,
        parsed_values,
        parsed_expressions,
        saved_variables,
    ))


def create__parse_target_name_param():
    return list(zip(
        targets,
        value,
        parsed_targets
    ))


def create__calculate_node_param():
    return list(zip(
        targets,
        value,
        parsed_values,
        parsed_expressions
    ))


def create__create_assign_viz_steps_param():
    return list(zip(
        targets,
        value,
        parsed_targets,
        parsed_expressions,
        expected_viz
    ))
