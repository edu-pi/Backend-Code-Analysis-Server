import ast
from unittest.mock import MagicMock, patch

import pytest

from app.visualize.analysis.stmt.models.expr_stmt_obj import ExprStmtObj
from app.visualize.analysis.stmt.models.for_stmt_obj import BodyObj
from app.visualize.analysis.stmt.models.if_stmt_obj import (
    IfStmtObj,
    IfConditionObj,
    ElifConditionObj,
    ElseConditionObj,
    ConditionObj,
)
from app.visualize.analysis.stmt.parser.expr.models.expr_obj import ExprObj, PrintObj
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
    print("a > 10")
elif a < 10:
    print("a < 10")
else:
    print("a > 10")
            """,
            IfStmtObj(
                conditions=(
                    IfConditionObj(id=1, expressions=("a>10",), result=False),
                    ElifConditionObj(id=2, expressions=("a<10",), result=False),
                    ElseConditionObj(id=3, expressions=None, result=True),
                ),
                body=BodyObj(body_steps=[[]], cur_value=0),
            ),
            id="complex if-elif-else",
        ),
    ],
)
def test_if_travel(code: str, expect, elem_manager):
    ast_if = ast.parse(code).body[0]
    with patch.object(
        IfStmt, "parse_if_condition", return_value=IfConditionObj(id=1, expressions=("a>10",), result=False)
    ), patch.object(
        IfStmt, "parse_elif_condition", return_value=ElifConditionObj(id=2, expressions=("a<10",), result=False)
    ), patch.object(
        IfStmt, "parse_else_condition", return_value=ElseConditionObj(id=3, expressions=None, result=True)
    ), patch.object(
        StmtTraveler, "_internal_travel", return_value=[]
    ):
        actual = StmtTraveler.if_travel(ast_if, [], [], elem_manager)
        assert actual == expect


@pytest.mark.parametrize(
    "conditions, node, expected",
    [
        pytest.param(
            [],
            ast.If(test=ast.parse("a > 10").body[0].value),
            IfConditionObj(id=1, expressions=("a>10",), result=False),
            id="conditions is empty",
        ),
        pytest.param(
            [IfConditionObj(id=1, expressions=("a>10",), result=False)],
            ast.If(test=ast.parse("True").body[0].value),
            ElifConditionObj(id=2, expressions=("a<10",), result=False),
            id="conditions is not empty",
        ),
    ],
)
def test_append_condition_obj(conditions, node, expected, elem_manager):
    with patch.object(
        IfStmt, "parse_if_condition", return_value=IfConditionObj(id=1, expressions=("a>10",), result=False)
    ), patch.object(
        IfStmt, "parse_elif_condition", return_value=ElifConditionObj(id=2, expressions=("a<10",), result=False)
    ):
        StmtTraveler._append_condition_obj(conditions, elem_manager, node)
        assert conditions[-1] == expected


@pytest.mark.parametrize(
    "conditions, node, result, expected",
    [
        pytest.param(
            [],
            ast.parse("print('hello')").body[0],
            True,
            ElseConditionObj(id=0, expressions=None, result=True),
            id="else condition when result True",
        ),
        pytest.param(
            [],
            ast.parse("print('hello')").body[0],
            False,
            ElseConditionObj(id=0, expressions=None, result=False),
            id="else condition when result False",
        ),
    ],
)
def test_append_else_condition_obj(conditions, node, result, expected):
    with patch.object(
        IfStmt,
        "parse_else_condition",
        side_effect=[
            ElseConditionObj(id=0, expressions=None, result=True),
            ElseConditionObj(id=0, expressions=None, result=False),
        ],
    ):
        StmtTraveler._append_else_condition_obj(conditions, node, result)
        assert conditions[-1].id == expected.id


@pytest.mark.parametrize(
    "node, conditions, body_objs",
    [
        pytest.param(
            ast.parse("if a > 10: \n    print('hello')").body[0],
            [IfConditionObj(id=1, expressions=("a>10",), result=True)],
            [],
            id="if condition is True - 바디 추가 함",
        ),
    ],
)
def test_parse_if_body_추가(node: ast.If, conditions: list[ConditionObj], body_objs: list[BodyObj], elem_manager):
    with patch.object(
        StmtTraveler,
        "_internal_travel",
        return_value=ExprStmtObj(id=0, expr_obj=PrintObj(value="hello", expressions=("hello",))),
    ):
        StmtTraveler._parse_if_body(node, conditions, body_objs, MagicMock())
        assert body_objs[-1] == ExprStmtObj(id=0, expr_obj=PrintObj(value="hello", expressions=("hello",)))


@pytest.mark.parametrize(
    "node, conditions, body_objs",
    [
        pytest.param(
            ast.parse("if a < 10: \n    print('hello')").body[0],
            [IfConditionObj(id=1, expressions=("a<10",), result=False)],
            [ExprStmtObj(id=0, expr_obj=PrintObj(value="hello", expressions=("hello",)))],
            id="if condition is False - 바디 추가 안함",
        )
    ],
)
def test_parse_if_body_추가_안함(node: ast.If, conditions: list[ConditionObj], body_objs: list[BodyObj], elem_manager):
    with patch.object(
        StmtTraveler,
        "_internal_travel",
        return_value=ExprStmtObj(id=0, expr_obj=PrintObj(value="hello", expressions=("hello",))),
    ):
        temp_body_objs = list(body_objs)
        StmtTraveler._parse_if_body(node, conditions, body_objs, MagicMock())
        assert temp_body_objs == body_objs
<<<<<<< HEAD
=======


def test_parse_if_orelse_elif문_분기_실행(elem_manager):
    body_objs = []
    conditions = [IfConditionObj(id=1, expressions=("a>10",), result=False)]
    if_node = ast.parse("if a < 10: \n    print('hello')\nelif a>10: \n   print('world')").body[0]

    with patch.object(StmtTraveler, "if_travel", return_value=None) as mock_if_travel:
        StmtTraveler._parse_if_branches(body_objs, conditions, elem_manager, if_node.orelse)

        mock_if_travel.assert_called_once()
        mock_if_travel.assert_called_with(if_node.orelse[0], conditions, body_objs, elem_manager)


def test_parse_if_orelse_else문_분기_실행(elem_manager):
    if_node = ast.parse("if a < 10: \n   print('world') \nelse: \n   print('world')").body[0]

    with patch.object(StmtTraveler, "_parse_else", return_value=None) as mock_if_travel:
        StmtTraveler._parse_if_branches([], [], elem_manager, if_node.orelse)

        mock_if_travel.assert_called_once()
        mock_if_travel.assert_called_with([], [], elem_manager, if_node.orelse)


@pytest.mark.parametrize(
    "target",
    [
        pytest.param(ast.Constant(value=10), id="10"),
        pytest.param(ast.Assign(targets=[ast.Name(id="a")], value=ast.Constant(value=10)), id="assign"),
    ],
)
def test_parse_if_orelse_예외발생(target, elem_manager):
    # 예외가 터지면 통과, 안터지면 실패
    with pytest.raises(TypeError):
        StmtTraveler._parse_if_branches([], [], elem_manager, target)
        assert False
>>>>>>> ef975c1 ([#141]test: StmtTraveler의 _parse_else 유닛 테스트)
