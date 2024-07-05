import pytest

from app.visualize.analysis.stmt.expr.model.expr_obj import PrintObj
from app.visualize.analysis.stmt.model.expr_stmt_obj import ExprStmtObj
from app.visualize.generator.converter.expr_converter import ExprConverter
from app.visualize.generator.model.models import PrintViz


@pytest.fixture
def create_print():
    def _create_print_obj(value, expressions):
        return ExprStmtObj(id=1, value=value, expressions=expressions, var_type="print")

    return _create_print_obj


@pytest.mark.parametrize(
    "value, expressions, expected",
    [
        pytest.param(
            "*\n",
            [
                "'*' * (i + 1)\n",
                "'*' * (0 + 1)\n",
                "*\n",
            ],
            [
                PrintViz(
                    id=1,
                    depth=1,
                    expr="'*' * (i + 1)\n",
                    highlights=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13],
                    console=None,
                ),
                PrintViz(
                    id=1,
                    depth=1,
                    expr="'*' * (0 + 1)\n",
                    highlights=[7],
                    console=None,
                ),
                PrintViz(
                    id=1,
                    depth=1,
                    expr="*\n",
                    highlights=[0, 1],
                    console="*\n",
                ),
            ],
            id="'*' * (i + 1): success case",
        )
    ],
)
def test_print_convert(create_print, value, expressions, expected):
    print_obj = create_print(value, expressions)
    result = ExprConverter._convert_to_print_viz(print_obj, 1, 1)

    assert result == expected
