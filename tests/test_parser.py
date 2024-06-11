import ast
import pytest

from app.analysis.element_manager import CodeElementManager
from app.analysis.models import Variables, Variable
from app.analysis.parser import assign_parse


def before_test():
    return [
        (  # a = 10
                [ast.Name(id="a", ctx=ast.Store)],
                ast.Constant(value=10),
                [Variables([Variable(depth=1, expr="10", name="a")])]
        ),
        (  # a = b = 10
                [ast.Name(id="a", ctx=ast.Store), ast.Name(id="b", ctx=ast.Store)],
                ast.Constant(value=10),
                [Variables(variable_list=[Variable(depth=1, expr="10", name='a'), Variable(depth=1, expr="10", name='b')], type='varList')]
        ),
        (  # a, b = 10, 14
                [ast.Tuple(elts=[ast.Name(id="a", ctx=ast.Store), ast.Name(id="b", ctx=ast.Store)], ctx=ast.Load)],
                ast.Tuple(elts=[ast.Constant(value=10), ast.Constant(value=14)]),
                [Variables(variable_list=[Variable(depth=1, expr="10", name='a'), Variable(depth=1, expr="14", name='b')], type='varList')]
        ),
    ]


@pytest.mark.parametrize("targets, value, expect", before_test())
def test_assign_parse(targets, value, expect):
    target_node = ast.Assign(targets=targets, value=value)

    g_elem_manager = CodeElementManager()
    steps = assign_parse(node=target_node, g_elem_manager=g_elem_manager)

    assert steps == expect



