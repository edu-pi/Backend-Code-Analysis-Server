import ast

import pytest

from app.visualize.analysis.stmt.expr.model.expr_obj import ExprObj
from app.visualize.analysis.stmt.model.assign_stmt_obj import AssignStmtObj
from app.visualize.analysis.stmt.parser.assign_stmt import AssignStmt


@pytest.mark.parametrize("code", ["a = 10", "abc = 10", "a = a + 1", "b = a + 1", "a = b = 10"])
def test_parse(create_ast, elem_manager, code):
    node = create_ast(code)
    result = AssignStmt.parse(node, elem_manager)

    assert isinstance(result, AssignStmtObj)


@pytest.mark.parametrize(
    "node, expected",
    [
        pytest.param(ast.Name(id="a", ctx=ast.Store()), "a", id="a = 10: success case"),
        pytest.param(ast.Name(id="abc", ctx=ast.Store()), "abc", id="abc = 10: success case"),
    ],
)
def test_get_target_name(elem_manager, node, expected):
    result = AssignStmt._get_target_name(node, elem_manager)

    assert result == expected


@pytest.mark.parametrize("target", [ast.Constant(value="abc")])
def test_get_target_name_fail(elem_manager, target):
    with pytest.raises(TypeError, match=r"\[AssignParser\]: .*는 잘못된 타입입니다."):
        AssignStmt._get_target_name(target, elem_manager)


@pytest.mark.parametrize(
    "node",
    [
        pytest.param(ast.Constant(value=10), id="a isinstance ExprObj: success case"),
        pytest.param(ast.Constant(value="abc"), id="abc isinstance ExprObj: success case"),
    ],
)
def test_change_node_to_expr_obj(elem_manager, node):
    result = AssignStmt._change_node_to_expr_obj(node, elem_manager)

    assert isinstance(result, ExprObj)
