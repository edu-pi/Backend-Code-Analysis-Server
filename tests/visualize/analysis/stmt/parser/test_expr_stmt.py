import ast

import pytest

from app.visualize.analysis.stmt.parser.expr.models.expr_obj import PrintObj, BinopObj, ConstantObj, NameObj
from app.visualize.analysis.stmt.parser.expr.models.expr_type import ExprType
from app.visualize.analysis.stmt.parser.expr_stmt import ExprStmt


@pytest.mark.parametrize(
    "node, expect",
    [
        pytest.param(
            ast.Name("a", ast.Load()),
            NameObj(value=10, expressions=("a", "10"), type=ExprType.VARIABLE),
            id="a: success case",
        ),
        pytest.param(
            ast.Constant(20),
            ConstantObj(
                value=20,
                expressions=("20",),
            ),
            id="20: success case",
        ),
        pytest.param(
            ast.BinOp(ast.Constant(10), ast.Add(), ast.Constant(20)),
            BinopObj(
                value=30,
                expressions=("10 + 20", "30"),
            ),
            id="10 + 20: success case",
        ),
        pytest.param(
            ast.Call(
                func=ast.Name("print", ast.Load()),
                args=[ast.BinOp(ast.Name("a", ast.Load()), ast.Add(), ast.Constant(2))],
                keywords=[],
            ),
            PrintObj(
                value="12\n",
                expressions=("a + 2", "10 + 2", "12"),
            ),
            id="print(a + 2): success case",
        ),
        pytest.param(
            ast.Call(
                func=ast.Name("print", ast.Load()),
                args=[ast.Name("a", ast.Load())],
                keywords=[],
            ),
            PrintObj(
                value="10\n",
                expressions=("a", "10"),
            ),
            id="print(a): success case",
        ),
    ],
)
def test__get_expr_obj(elem_container, node, expect):
    # expr 노드를 받아서 변수 이름을 반환하는지 통합테스트
    actual = ExprStmt._get_expr_obj(node, elem_container)

    assert actual == expect
