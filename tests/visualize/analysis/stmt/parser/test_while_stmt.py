import ast

import pytest

from app.visualize.analysis.stmt.parser.expr.expr_traveler import ExprTraveler
from app.visualize.analysis.stmt.parser.expr.models.expr_obj import CompareObj, NameObj, ConstantObj, ExprObj
from app.visualize.analysis.stmt.parser.expr.models.expr_type import ExprType
from app.visualize.analysis.stmt.parser.while_stmt import WhileStmt


@pytest.mark.parametrize(
    "test_node, test_obj",
    [
        pytest.param(
            ast.Compare(left=ast.Num(n=3), ops=[ast.Lt()], comparators=[ast.Num(n=10)]),
            CompareObj(expressions=("3 < 10", "True"), value=True),
            id="3 < 10: success case",
        ),
        pytest.param(
            ast.Name(id="a", ctx=ast.Load()),
            NameObj(expressions=("a", "10"), value=10, type=ExprType.VARIABLE),
            id="a: success case",
        ),
    ],
)
def test_parse_condition(mocker, elem_container, test_node: ast.expr, test_obj):
    mock_expr_traveler = mocker.patch.object(ExprTraveler, "travel", return_value=test_obj)
    mock_while_stmt = mocker.patch.object(WhileStmt, "_add_last_bool_expression")

    result = WhileStmt.parse_condition(test_node, elem_container)

    mock_expr_traveler.assert_called_once_with(test_node, elem_container)
    mock_while_stmt.assert_called_once_with(test_obj)


@pytest.mark.parametrize(
    "test_obj, expected",
    [
        pytest.param(
            CompareObj(expressions=("3 < 10", "True"), value=True),
            CompareObj(expressions=("3 < 10", "True"), value=True),
            id="last expression is True",
        ),
        pytest.param(
            ConstantObj(expressions=("False",), value=False),
            ConstantObj(expressions=("False",), value=False),
            id="last expression is False",
        ),
        pytest.param(
            NameObj(expressions=("a", "10"), value=10, type=ExprType.VARIABLE),
            NameObj(expressions=("a", "10", "True"), value=10, type=ExprType.VARIABLE),
            id="last expression is not bool",
        ),
    ],
)
def test__add_last_bool_expression(test_obj: ExprObj, expected):
    result = WhileStmt._add_last_bool_expression(test_obj)

    assert result == expected
