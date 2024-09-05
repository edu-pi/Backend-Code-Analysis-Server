import ast

import pytest

from app.visualize.analysis.stmt.parser.expr.models.expr_obj import ExprObj, ConstantObj, NameObj
from app.visualize.analysis.stmt.parser.expr.models.expr_type import ExprType
from app.visualize.analysis.stmt.parser.expr.parser.unary_op_expr import UnaryOpExpr


@pytest.mark.parametrize(
    "op, operand, expected",
    [
        pytest.param(
            ast.Invert(),
            ConstantObj(value=5, expressions=("5",)),
            ~5,
            id="Invert ~5: success case",
        ),
        pytest.param(
            ast.Not(),
            ConstantObj(value=5, expressions=("5",)),
            not 5,
            id="Not not 5: success case",
        ),
        pytest.param(
            ast.UAdd(),
            ConstantObj(value=5, expressions=("5",)),
            +5,
            id="UAdd +5: success case",
        ),
        pytest.param(
            ast.USub(),
            ConstantObj(value=5, expressions=("5",)),
            -5,
            id="USub -5: success case",
        ),
        pytest.param(
            ast.USub(),
            NameObj(value=5, expressions=("a", "5"), type=ExprType.VARIABLE),
            -5,
            id="USub -a: success case",
        ),
    ],
)
def test_get_value(op: ast, operand: ExprObj, expected):
    result = UnaryOpExpr._get_value(op, operand)
    assert result == expected


@pytest.mark.parametrize(
    "op, operand, expected",
    [
        pytest.param(
            ast.Invert(),
            ConstantObj(value=5, expressions=("5",)),
            ("~5",),
            id="Invert ~5: success case",
        ),
        pytest.param(
            ast.Not(),
            ConstantObj(value=5, expressions=("5",)),
            ("not 5",),
            id="Not not 5: success case",
        ),
        pytest.param(
            ast.UAdd(),
            ConstantObj(value=5, expressions=("5",)),
            ("+5",),
            id="UAdd +5: success case",
        ),
        pytest.param(
            ast.USub(),
            ConstantObj(value=5, expressions=("5",)),
            ("-5",),
            id="USub -5: success case",
        ),
        pytest.param(
            ast.USub(),
            NameObj(value=5, expressions=("a", "5"), type=ExprType.VARIABLE),
            ("-a", "-5"),
            id="USub -a: success case",
        ),
    ],
)
def test_concat_expressions(op: ast, operand: ExprObj, expected):
    result = UnaryOpExpr._concat_expressions(op, operand)
    assert result == expected
