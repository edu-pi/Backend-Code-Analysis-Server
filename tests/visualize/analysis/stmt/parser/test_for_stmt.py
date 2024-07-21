import ast
import pytest


from app.visualize.analysis.stmt.models.assign_stmt_obj import AssignStmtObj
from app.visualize.analysis.stmt.models.expr_stmt_obj import ExprStmtObj
from app.visualize.analysis.stmt.models.flow_control_obj import BreakStmtObj
from app.visualize.analysis.stmt.models.for_stmt_obj import BodyObj
from app.visualize.analysis.stmt.models.if_stmt_obj import IfStmtObj, ConditionObj
from app.visualize.analysis.stmt.parser.expr.models.expr_obj import ExprObj
from app.visualize.analysis.stmt.parser.for_stmt import ForStmt


@pytest.mark.parametrize(
    "target, expect",
    [
        pytest.param(ast.Name(id="i", ctx=ast.Store()), "i", id="i"),
        pytest.param(ast.Name(id="a", ctx=ast.Store()), "a", id="a"),
    ],
)
def test__get_target_name(elem_container, target, expect):
    # target 노드를 받아서 변수 이름을 반환하는지 테스트
    result = ForStmt._get_target_name(target, elem_container)
    assert result == expect


@pytest.mark.parametrize(
    "target",
    [
        (ast.Constant(value=1)),
    ],
)
def test__get_target_name_fail(elem_container, target):
    # target 노드를 받아서 변수 이름을 반환하는지 테스트
    # 예외가 터지면 통과, 안터지면 실
    with pytest.raises(TypeError, match=r"\[ForParser\]:  .*는 잘못된 타입입니다."):
        ForStmt._get_target_name(target, elem_container)


@pytest.mark.parametrize(
    "body_steps",
    [
        pytest.param(
            [
                AssignStmtObj(targets=(), expr_stmt_obj=ExprStmtObj(id=1, value="", expressions=("",), expr_type="")),
                IfStmtObj(
                    conditions=(ConditionObj(id=0, expressions=("",), result=True, type="if"),),
                    body_steps=[
                        BreakStmtObj(id=0, expr="break"),
                    ],
                ),
                AssignStmtObj(targets=(), expr_stmt_obj=ExprStmtObj(id=1, value="", expressions=("",), expr_type="")),
            ],
            id="for문 안에 break 존재",
        ),
        pytest.param(
            [
                AssignStmtObj(targets=(), expr_stmt_obj=ExprStmtObj(id=1, value="", expressions=("",), expr_type="")),
                BreakStmtObj(id=0, expr="break"),
                AssignStmtObj(targets=(), expr_stmt_obj=ExprStmtObj(id=1, value="", expressions=("",), expr_type="")),
            ],
            id="for문의 if문안에 break 존재",
        ),
    ],
)
def test_contains_break_success(body_steps):
    # stmt list에서 break가 존재하는지 확인
    actual = ForStmt.contains_break(body_steps)

    assert actual is True


@pytest.mark.parametrize(
    "body_steps",
    [
        pytest.param(
            [
                AssignStmtObj(targets=(), expr_stmt_obj=ExprStmtObj(id=1, value="", expressions=("",), expr_type="")),
                IfStmtObj(
                    conditions=(ConditionObj(id=0, expressions=("",), result=True, type="if"),),
                    body_steps=[
                        AssignStmtObj(
                            targets=(), expr_stmt_obj=ExprStmtObj(id=1, value="", expressions=("",), expr_type="")
                        ),
                    ],
                ),
                AssignStmtObj(targets=(), expr_stmt_obj=ExprStmtObj(id=1, value="", expressions=("",), expr_type="")),
            ],
            id="for문 안에 break 미존재",
        ),
        pytest.param(
            [
                AssignStmtObj(targets=(), expr_stmt_obj=ExprStmtObj(id=1, value="", expressions=("",), expr_type="")),
                AssignStmtObj(targets=(), expr_stmt_obj=ExprStmtObj(id=1, value="", expressions=("",), expr_type="")),
            ],
            id="for문의 if문안에 break 미존재",
        ),
    ],
)
def test_contains_break_fail(body_steps):
    # stmt list에서 break가 존재하는지 확인
    actual = ForStmt.contains_break(body_steps)

    assert actual is False


@pytest.mark.parametrize(
    "body_objs, expected",
    [
        pytest.param(
            [
                AssignStmtObj(targets=(), expr_stmt_obj=ExprStmtObj(id=1, value="", expressions=("",), expr_type="")),
                IfStmtObj(
                    conditions=(ConditionObj(id=0, expressions=("",), result=True, type="if"),),
                    body_steps=[
                        AssignStmtObj(
                            targets=(), expr_stmt_obj=ExprStmtObj(id=1, value="", expressions=("",), expr_type="")
                        ),
                        BreakStmtObj(id=0, expr="break"),
                        AssignStmtObj(
                            targets=(), expr_stmt_obj=ExprStmtObj(id=1, value="", expressions=("",), expr_type="")
                        ),
                    ],
                ),
                AssignStmtObj(targets=(), expr_stmt_obj=ExprStmtObj(id=1, value="", expressions=("",), expr_type="")),
            ],
            [
                AssignStmtObj(targets=(), expr_stmt_obj=ExprStmtObj(id=1, value="", expressions=("",), expr_type="")),
                IfStmtObj(
                    conditions=(ConditionObj(id=0, expressions=("",), result=True, type="if"),),
                    body_steps=[
                        AssignStmtObj(
                            targets=(), expr_stmt_obj=ExprStmtObj(id=1, value="", expressions=("",), expr_type="")
                        ),
                        BreakStmtObj(id=0, expr="break"),
                    ],
                ),
            ],
            id="break가 if문 내부에 존재할 때",
        ),
        pytest.param(
            [
                AssignStmtObj(targets=(), expr_stmt_obj=ExprStmtObj(id=1, value="", expressions=("",), expr_type="")),
                IfStmtObj(
                    conditions=(ConditionObj(id=0, expressions=("",), result=True, type="if"),),
                    body_steps=[
                        AssignStmtObj(
                            targets=(), expr_stmt_obj=ExprStmtObj(id=1, value="", expressions=("",), expr_type="")
                        ),
                        AssignStmtObj(
                            targets=(), expr_stmt_obj=ExprStmtObj(id=1, value="", expressions=("",), expr_type="")
                        ),
                    ],
                ),
                BreakStmtObj(id=0, expr="break"),
                AssignStmtObj(targets=(), expr_stmt_obj=ExprStmtObj(id=1, value="", expressions=("",), expr_type="")),
            ],
            [
                AssignStmtObj(targets=(), expr_stmt_obj=ExprStmtObj(id=1, value="", expressions=("",), expr_type="")),
                IfStmtObj(
                    conditions=(ConditionObj(id=0, expressions=("",), result=True, type="if"),),
                    body_steps=[
                        AssignStmtObj(
                            targets=(), expr_stmt_obj=ExprStmtObj(id=1, value="", expressions=("",), expr_type="")
                        ),
                        AssignStmtObj(
                            targets=(), expr_stmt_obj=ExprStmtObj(id=1, value="", expressions=("",), expr_type="")
                        ),
                    ],
                ),
                BreakStmtObj(id=0, expr="break"),
            ],
            id="break가 for문 내부에 존재할 때",
        ),
        pytest.param(
            [
                AssignStmtObj(targets=(), expr_stmt_obj=ExprStmtObj(id=1, value="", expressions=("",), expr_type="")),
                IfStmtObj(
                    conditions=(ConditionObj(id=0, expressions=("",), result=True, type="if"),),
                    body_steps=[
                        AssignStmtObj(
                            targets=(), expr_stmt_obj=ExprStmtObj(id=1, value="", expressions=("",), expr_type="")
                        ),
                        AssignStmtObj(
                            targets=(), expr_stmt_obj=ExprStmtObj(id=1, value="", expressions=("",), expr_type="")
                        ),
                    ],
                ),
                AssignStmtObj(targets=(), expr_stmt_obj=ExprStmtObj(id=1, value="", expressions=("",), expr_type="")),
            ],
            [
                AssignStmtObj(targets=(), expr_stmt_obj=ExprStmtObj(id=1, value="", expressions=("",), expr_type="")),
                IfStmtObj(
                    conditions=(ConditionObj(id=0, expressions=("",), result=True, type="if"),),
                    body_steps=[
                        AssignStmtObj(
                            targets=(), expr_stmt_obj=ExprStmtObj(id=1, value="", expressions=("",), expr_type="")
                        ),
                        AssignStmtObj(
                            targets=(), expr_stmt_obj=ExprStmtObj(id=1, value="", expressions=("",), expr_type="")
                        ),
                    ],
                ),
                AssignStmtObj(targets=(), expr_stmt_obj=ExprStmtObj(id=1, value="", expressions=("",), expr_type="")),
            ],
            id="break가 존재하지 않을 때",
        ),
    ],
)
def test_get_pre_break_body_steps(body_objs, expected):
    actual = ForStmt.get_pre_break_body_steps(body_objs)

    assert actual == expected
