import ast
from unittest.mock import MagicMock

import pytest

from app.visualize.container.element_container import ElementContainer
from app.visualize.analysis.stmt.expr.models.expr_obj import ExprObj
from app.visualize.analysis.stmt.stmt_traveler import StmtTraveler


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
                expressions=[{"end": "3", "start": "0", "step": "1"}],
            ),
        )
    ],
)
def test_for_travel(create_ast, code, expect, elem_manager):
    actual = StmtTraveler.for_travel(create_ast(code), elem_manager)
    pass
