import pytest

from app.visualize.analysis.stmt.models.if_stmt_obj import IfConditionObj, ElifConditionObj, ElseConditionObj
from app.visualize.analysis.stmt.parser.expr.expr_traveler import ExprTraveler
from app.visualize.analysis.stmt.parser.expr.models.expr_obj import CompareObj
from app.visualize.analysis.stmt.parser.if_stmt import IfStmt


@pytest.mark.parametrize(
    "input_code, expected, travel_return_value",
    [
        pytest.param(
            "a>10",
            IfConditionObj(id=1, expressions=("a>10",), result=False),
            CompareObj(expressions=("a>10",), value=False),
            id="a>10",
        ),
        pytest.param(
            "a>b",
            IfConditionObj(id=1, expressions=("a>b", "10>9"), result=True),
            CompareObj(expressions=("a>b", "10>9"), value=True),
            id="a>b",
        ),
    ],
)
def test_parse_if_condition(mocker, input_code, expected, travel_return_value, create_ast, elem_manager):
    test_node = create_ast(input_code).value
    mocker.patch.object(ExprTraveler, "travel", return_value=travel_return_value),

    actual = IfStmt.parse_if_condition(test_node, elem_manager)

    assert actual == expected


@pytest.mark.parametrize(
    "input_code, expected, travel_return_value",
    [
        pytest.param(
            "a>10",
            ElifConditionObj(id=1, expressions=("a>10", "10>10", "False"), result=False),
            CompareObj(expressions=("a>10", "10>10"), value=False),
            id="a>10",
        ),
        pytest.param(
            "a>b",
            ElifConditionObj(id=1, expressions=("a>b", "10>9", "True"), result=True),
            CompareObj(expressions=("a>b", "10>9"), value=True),
            id="a>b",
        ),
    ],
)
def test_parse_elif_condition(mocker, create_ast, elem_container, input_code, expected, travel_return_value):
    test_node = create_ast(input_code).value
    mocker.patch.object(ExprTraveler, "travel", return_value=travel_return_value)

    actual = IfStmt.parse_elif_condition(test_node, elem_container)

    assert actual == expected


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

    actual = IfStmt.parse_else_condition(else_body_node, True)

    assert actual == expected
