import ast

import pytest

from app.visualize.analysis.stmt.parser.expr.models.expr_obj import ExprObj
from app.visualize.analysis.stmt.models.assign_stmt_obj import AssignStmtObj
from app.visualize.analysis.stmt.parser.assign_stmt import AssignStmt


@pytest.mark.parametrize("code", ["a = 10", "abc = 10", "a = a + 1", "b = a + 1", "a = b = 10"])
def test_parse(create_ast, elem_container, code):
    node = create_ast(code)
    result = AssignStmt.parse(node, elem_container)

    assert isinstance(result, AssignStmtObj)


@pytest.mark.parametrize(
    "node, expected",
    [
        pytest.param(ast.Name(id="a", ctx=ast.Store()), "a", id="a = 10: success case"),
        pytest.param(ast.Name(id="abc", ctx=ast.Store()), "abc", id="abc = 10: success case"),
    ],
)
def test_get_target_name(elem_container, node, expected):
    result = AssignStmt._get_target_name(node, elem_container)

    assert result == expected


@pytest.mark.parametrize("target", [ast.Constant(value="abc")])
def test_get_target_name_fail(elem_container, target):
    with pytest.raises(TypeError, match=r"\[AssignParser\]: .*는 잘못된 타입입니다."):
        AssignStmt._get_target_name(target, elem_container)


@pytest.mark.parametrize(
    "node",
    [
        pytest.param(ast.Constant(value=10), id="a isinstance ExprObj: success case"),
        pytest.param(ast.Constant(value="abc"), id="abc isinstance ExprObj: success case"),
    ],
)
def test_change_node_to_expr_obj(elem_container, node):
    result = AssignStmt._change_node_to_expr_obj(node, elem_container)

    assert isinstance(result, ExprObj)
