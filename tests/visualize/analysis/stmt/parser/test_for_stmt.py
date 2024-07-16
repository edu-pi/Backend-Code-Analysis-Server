import ast
import pytest

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
