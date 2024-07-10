import ast
from unittest.mock import MagicMock, patch

import pytest

from app.visualize.analysis.stmt.models.if_stmt_obj import IfConditionObj, ElifConditionObj, ElseConditionObj
from app.visualize.analysis.stmt.parser.expr.expr_traveler import ExprTraveler
from app.visualize.analysis.stmt.parser.expr.models.expr_obj import CompareObj
from app.visualize.analysis.stmt.parser.if_stmt import IfStmt
from app.visualize.container.element_container import ElementContainer


@pytest.fixture
def create_ast():
    # 코드를 ast 노드로 변환하는 함수를 반환
    def _create_ast_node(code):
        # ast.Call 반환
        return ast.parse(code).body[0]

    return _create_ast_node


@pytest.mark.parametrize(
    "input_code, expected, travel_return_value, evaluate_test_value_return",
    [
        pytest.param(
            "a>10",
            IfConditionObj(id=1, expressions=("a>10",), result=False),
            CompareObj(expressions=("a>10",), value="10>10"),
            False,
            id="a>10",
        ),
        pytest.param(
            "a>b",
            IfConditionObj(id=1, expressions=("a>b", "10>9"), result=True),
            CompareObj(expressions=("a>b", "10>9"), value="10>9"),
            True,
            id="a>b",
        ),
    ],
)
def test_parse_if_condition(
    input_code, expected, travel_return_value, evaluate_test_value_return, create_ast, elem_manager
):
    test_node = create_ast(input_code).value
    with (
        patch.object(ExprTraveler, "travel", return_value=travel_return_value),
        patch.object(IfStmt, "_evaluate_test_value", return_value=evaluate_test_value_return),
    ):
        assert IfStmt.parse_if_condition(test_node, elem_manager) == expected


@pytest.mark.parametrize(
    "input_code, expected, travel_return_value, evaluate_test_value_return",
    [
        pytest.param(
            "a>10",
            ElifConditionObj(id=1, expressions=("a>10",), result=False),
            CompareObj(expressions=("a>10",), value="10>10"),
            False,
            id="a>10",
        ),
        pytest.param(
            "a>b",
            ElifConditionObj(id=1, expressions=("a>b", "10>9"), result=True),
            CompareObj(expressions=("a>b", "10>9"), value="10>9"),
            True,
            id="a>b",
        ),
    ],
)
def test_parse_elif_condition(
    input_code, expected, travel_return_value, evaluate_test_value_return, create_ast, elem_container
):
    test_node = create_ast(input_code).value
    with (
        patch.object(ExprTraveler, "travel", return_value=travel_return_value),
        patch.object(IfStmt, "_evaluate_test_value", return_value=evaluate_test_value_return),
    ):
        assert IfStmt.parse_elif_condition(test_node, elem_container) == expected


@pytest.mark.parametrize(
    "input_code, expected",
    [
        pytest.param(
            "a=10",
            ElseConditionObj(id=0, expressions=None, result=True),
            id="a>10",
        ),
        pytest.param(
            "a=b",
            ElseConditionObj(id=0, expressions=None, result=True),
            id="a>b",
        ),
    ],
)
def test_parse_if_condition(input_code, expected, create_ast):
    else_body_node = create_ast(input_code).value

    assert IfStmt.parse_else_condition(else_body_node, True) == expected


@pytest.mark.parametrize(
    "input_code, expected",
    [
        pytest.param(
            "a > 10",
            False,
            id="a > 10",
        ),
        pytest.param(
            "a == 10",
            True,
            id="a == 10",
        ),
        pytest.param(
            "a == b",
            False,
            id="a == b",
        ),
        pytest.param(
            "a < b",
            True,
            id="a < b",
        ),
    ],
)
def test__evaluate_test_value(input_code: str, expected):
    test_node = ast.parse(input_code).body[0].value
    elem_manager = MagicMock(spec=ElementContainer)
    elem_manager.get_element_dict.return_value = {"a": 10, "b": 12}

    assert IfStmt._evaluate_test_value(test_node, elem_manager) == expected
