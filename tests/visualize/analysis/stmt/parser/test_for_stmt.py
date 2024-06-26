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
def test_get_condition_value_list(create_ast, elem_manager, code, expect):
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
