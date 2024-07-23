import ast

import pytest

from app.visualize.analysis.stmt.models.assign_stmt_obj import AssignStmtObj
from app.visualize.analysis.stmt.parser.expr.expr_traveler import ExprTraveler
from app.visualize.analysis.stmt.parser.expr.models.expr_obj import (
    ExprObj,
    NameObj,
    TupleObj,
    ListObj,
    ConstantObj,
    BinopObj,
)
from app.visualize.analysis.stmt.parser.assign_stmt import AssignStmt
from app.visualize.analysis.stmt.parser.expr.models.expr_type import ExprType


@pytest.mark.parametrize(
    "code, mock_target_names, mock_expr_obj",
    [
        pytest.param(
            "a = 10",
            ("a",),
            ConstantObj(value=10, expressions=("10",)),
            id="a = 10: success case",
        ),
        pytest.param(
            "a = a + 1",
            ("a",),
            BinopObj(value=11, expressions=("a + 1", "10 + 1", "11")),
            id="a = a + 1: success case",
        ),
        pytest.param(
            "a = b = 10",
            ("a", "b"),
            ConstantObj(value=10, expressions=("10",)),
            id="a = b = 10: success case",
        ),
    ],
)
def test_parse(mocker, create_ast, elem_container, code, mock_target_names, mock_expr_obj):
    mock_get_target_names = mocker.patch.object(AssignStmt, "_get_target_names", return_value=mock_target_names)
    mock_change_node_to_expr_obj = mocker.patch.object(
        AssignStmt, "_change_node_to_expr_obj", return_value=mock_expr_obj
    )
    mock_set_value_to_target = mocker.patch.object(AssignStmt, "_set_value_to_target")
    node = create_ast(code)

    result = AssignStmt.parse(node, elem_container)

    assert isinstance(result, AssignStmtObj)
    mock_get_target_names.assert_called_once_with(node.targets, elem_container)
    mock_change_node_to_expr_obj.assert_called_once_with(node.value, elem_container)
    mock_set_value_to_target.assert_called_once_with(mock_target_names, mock_expr_obj, elem_container)


@pytest.mark.parametrize(
    "target_nodes, expected",
    [
        pytest.param(
            [ast.Name(id="a", ctx=ast.Store())],
            (NameObj(value="a", expressions=("a",), type=ExprType.NAME),),
            id="a = 10: success case",
        ),
        pytest.param(
            [ast.Name(id="abc", ctx=ast.Store())],
            (NameObj(value="abc", expressions=("abc",), type=ExprType.NAME),),
            id="abc = 10: success case",
        ),
        pytest.param(
            [ast.Tuple(elts=[ast.Name(id="a", ctx=ast.Store()), ast.Name(id="b", ctx=ast.Store())])],
            (TupleObj(value=("a", "b"), expressions=("('a', 'b')",)),),
            id="a, b = 10: success case",
        ),
        pytest.param(
            [ast.List(elts=[ast.Name(id="a", ctx=ast.Store()), ast.Name(id="b", ctx=ast.Store())])],
            (ListObj(value=["a", "b"], expressions=("['a', 'b']",)),),
            id="[a, b] = 10: success case",
        ),
        pytest.param(
            [
                ast.Name(id="a", ctx=ast.Store()),
                ast.List(elts=[ast.Name(id="b", ctx=ast.Store()), ast.Name(id="c", ctx=ast.Store())]),
            ],
            (
                NameObj(value="a", expressions=("a",), type=ExprType.NAME),
                ListObj(value=["b", "c"], expressions=("['b', 'c']",)),
            ),
            id="a = b, c = 10, 12: success case",
        ),
    ],
)
def test_get_target_names(mocker, elem_container, target_nodes: list[ast], expected: tuple):
    mock_expr_traveler = mocker.patch.object(ExprTraveler, "travel", side_effect=[expr_obj for expr_obj in expected])

    result = AssignStmt._get_target_names(target_nodes, elem_container)

    assert result == tuple([expr_obj.value for expr_obj in expected])
    assert mock_expr_traveler.call_count == len(target_nodes)


@pytest.mark.parametrize("target_nodes", [[ast.Constant(value="abc")]])
def test_get_target_name_fail(elem_container, target_nodes):
    with pytest.raises(TypeError, match=r"\[AssignParser\]: .*는 잘못된 타입입니다."):
        AssignStmt._get_target_names(target_nodes, elem_container)


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
