import ast

import pytest

from app.visualize.analysis.stmt.expr.model.expr_obj import ExprObj
from app.visualize.analysis.stmt.parser.expr_stmt import ExprStmt


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
            """a""",
            ExprObj(
                type="name",
                value=10,
                expressions=["a", "10"],
            ),
        ),
        (
            """20""",
            ExprObj(
                type="constant",
                value=20,
                expressions=["20"],
            ),
        ),
        (
            """10 + 20""",
            ExprObj(
                type="binop",
                value=30,
                expressions=["10 + 20", "30"],
            ),
        ),
        (
            """print(a+2)""",
            ExprObj(
                type="print",
                value="12\n",
                expressions=["a + 2\n", "10 + 2\n", "12\n"],
            ),
        ),
        (
            """print(a)""",
            ExprObj(
                type="print",
                value="10\n",
                expressions=["a\n", "10\n"],
            ),
        ),
    ],
)
def test__get_expr_obj(create_ast, elem_manager, code, expect):
    # expr 노드를 받아서 변수 이름을 반환하는지 통합테스트
    expr_node = create_ast(code)

    actual = ExprStmt._get_expr_obj(expr_node.value, elem_manager)
    assert actual == expect
