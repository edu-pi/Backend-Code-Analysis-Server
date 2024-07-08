import ast
from unittest.mock import MagicMock, patch

import pytest

from app.visualize.analysis.stmt.models.for_stmt_obj import BodyObj
from app.visualize.analysis.stmt.models.if_stmt_obj import IfStmtObj, IfConditionObj, ElifConditionObj, ElseConditionObj
from app.visualize.analysis.stmt.parser.expr.models.expr_obj import ExprObj
from app.visualize.analysis.stmt.parser.if_stmt import IfStmt
from app.visualize.analysis.stmt.stmt_traveler import StmtTraveler
from app.visualize.container.element_container import ElementContainer


@pytest.fixture
def create_ast():
    # 코드를 ast 노드로 변환하는 함수를 반환
    def _create_ast_node(code):
        # ast.Call 반환
        return ast.parse(code).body[0]

    return _create_ast_node


@pytest.fixture
def elem_manager():
    mock = MagicMock(spec=ElementContainer)
    return mock


@pytest.mark.parametrize(
    "code, expect",
    [
        (
            """for i in range(3): \n    print('hello')""",
            ExprObj(
                type="for",
                value={"end": "3", "start": "0", "step": "1"},
                expressions=({"end": "3", "start": "0", "step": "1"},),
            ),
        )
    ],
)
def test_for_travel(create_ast, code, expect, elem_manager):
    actual = StmtTraveler._for_travel(create_ast(code), elem_manager)
    pass


@pytest.mark.parametrize(
    "code, expect",
    [
        pytest.param(
            """
if a > 10:
    pass
elif a < 10:
    pass
elif a < 12:
    pass
else:
    pass
            """,
            IfStmtObj(
                conditions=(
                    IfConditionObj(id=1, expressions=("a>10",), result=False),
                    ElifConditionObj(id=2, expressions=("a<10",), result=False),
                    ElifConditionObj(id=3, expressions=("a<12",), result=False),
                    ElseConditionObj(id=4, expressions=None, result=True),
                ),
                body=BodyObj(body_steps=[[]], cur_value=0),
            ),
            id="complex if-elif-else",
        ),
    ],
)
def test_if_travel(code, expect, elem_manager):
    ast_if = ast.parse(code).body[0]
    with patch.object(
        IfStmt, "parse_if_condition", return_value=IfConditionObj(id=1, expressions=("a>10",), result=False)
    ), patch.object(
        IfStmt,
        "parse_elif_condition",
        side_effect=[
            ElifConditionObj(id=2, expressions=("a<10",), result=False),
            ElifConditionObj(id=3, expressions=("a<12",), result=False),
        ],
    ), patch.object(
        IfStmt, "parse_else_condition", return_value=ElseConditionObj(id=4, expressions=None, result=True)
    ), patch.object(
        StmtTraveler, "_internal_travel", return_value=[]
    ):
        actual = StmtTraveler.if_travel(ast_if, [], [], elem_manager)
        assert actual == expect
