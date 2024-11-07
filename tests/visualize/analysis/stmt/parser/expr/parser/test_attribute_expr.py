import pytest

from app.visualize.analysis.stmt.parser.expr.models.expr_obj import NameObj, AttributeObj, ExprObj, ListObj
from app.visualize.analysis.stmt.parser.expr.models.expr_type import ExprType
from app.visualize.analysis.stmt.parser.expr.parser.attribute_expr import AttributeExpr

target_list = [1, 2, 3, 4, 5]


@pytest.mark.parametrize(
    "target_obj, attr_name, expected",
    [
        pytest.param(
            NameObj(value=target_list, expressions=("a", "[1, 2, 3, 4, 5]"), type=ExprType.LIST),
            "append",
            AttributeObj(
                value=getattr(target_list, "append"),
                expressions=("a", "[1, 2, 3, 4, 5]"),
                type=ExprType.APPEND,
            ),
            id="a.append(10): success case",
        ),
        pytest.param(
            ListObj(value=target_list, expressions=("[1, 2, 3, 4, 5]",)),
            "append",
            AttributeObj(
                value=getattr(target_list, "append"),
                expressions=("[1, 2, 3, 4, 5]",),
                type=ExprType.APPEND,
            ),
            id="[1, 2, 3, 4, 5].append(10): success case",
        ),
    ],
)
def test_parse_append_case(target_obj: ExprObj, attr_name: str, expected):
    result = AttributeExpr.parse(target_obj, attr_name)

    assert result == expected
