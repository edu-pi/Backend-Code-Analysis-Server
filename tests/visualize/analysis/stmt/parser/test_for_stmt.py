import ast
from unittest.mock import MagicMock, patch
import pytest

from app.visualize.analysis.stmt.expr.model.expr_obj import ExprObj
from app.visualize.analysis.stmt.parser.for_stmt import ForStmt
from app.visualize.analysis.stmt.parser.expr_stmt import ExprTraveler


@pytest.fixture
def create_ast():
    # 코드를 ast 노드로 변환하는 함수를 반환
    def _create_ast_node(code):
        # ast.Call 반환
        return ast.parse(code).body[0]

    return _create_ast_node


@pytest.mark.parametrize(
    "code, expect",
    [
        (
            """for i in range(3): \n    pass""",
            ExprObj(
                type="name",
                value="i",
                expressions=["i"],
            ),
        ),
        (
            """for a in range(3): \n    pass""",
            ExprObj(
                type="name",
                value="a",
                expressions=["a"],
            ),
        ),
    ],
)
def test__get_target_name(create_ast, elem_manager, code, expect):
    # target 노드를 받아서 변수 이름을 반환하는지 테스트
    target_node = create_ast(code).target

    actual = ForStmt._get_target_name(target_node, elem_manager)
    assert actual == expect


@pytest.mark.parametrize(
    "code, expect",
    [
        (
            """for [a] in range(10): \n    pass""",
            ExprObj(
                type="name",
                value="i",
                expressions=["i"],
            ),
        ),
    ],
)
def test__get_target_name_fail(create_ast, elem_manager, code, expect):
    # target 노드를 받아서 변수 이름을 반환하는지 테스트
    target_node = create_ast(code).target

    # 예외가 터지면 통과, 안터지면 실패
    with pytest.raises(TypeError, match=r"\[ForParser\]:  .*는 잘못된 타입입니다."):
        ForStmt._get_target_name(target_node, elem_manager)


# TODO 함수마다 parser를 추가하는 방향 고민
@pytest.mark.parametrize(
    "code, expect",
    [
        (
            """for i in range(3): \n    pass""",
            ExprObj(
                type="range",
                value={"end": "3", "start": "0", "step": "1"},
                expressions=[{"end": "3", "start": "0", "step": "1"}],
            ),
        )
    ],
)
def test_get_condition_obj(create_ast, elem_manager, code, expect):
    # iter 노드를 받아서 range 함수의 파라미터를 반환하는지 테스트
    iter_node = create_ast(code).iter

    with patch.object(
        ExprTraveler,
        "call_travel",
        return_value=ExprObj(
            type="range",
            value={"end": "3", "start": "0", "step": "1"},
            expressions=[{"end": "3", "start": "0", "step": "1"}],
        ),
    ):
        actual = ForStmt._get_condition_obj(iter_node, elem_manager)
        assert actual == expect
