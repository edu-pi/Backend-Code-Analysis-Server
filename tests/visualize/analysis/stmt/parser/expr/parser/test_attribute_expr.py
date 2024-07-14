import pytest

from app.visualize.analysis.stmt.parser.expr.models.expr_obj import NameObj, ConstantObj, AttributeObj, ExprObj, ListObj
from app.visualize.analysis.stmt.parser.expr.parser.attribute_expr import AttributeExpr


@pytest.mark.parametrize(
    "target_obj, attr_name, arg_objs, expected",
    [
        pytest.param(
            NameObj(value=[1, 2, 3, 4, 5], expressions=("a", "[1, 2, 3, 4, 5]")),
            "append",
            [ConstantObj(value=10, expressions=("10",))],
            AttributeObj(value=[1, 2, 3, 4, 5, 10], expressions=("[1, 2, 3, 4, 5]", "[1, 2, 3, 4, 5, 10]")),
            id="a.append(10): success case",
        ),
        pytest.param(
            ListObj(value=[1, 2, 3, 4, 5], expressions=("[1, 2, 3, 4, 5]",)),
            "append",
            [ConstantObj(value=10, expressions=("10",))],
            AttributeObj(value=[1, 2, 3, 4, 5, 10], expressions=("[1, 2, 3, 4, 5]", "[1, 2, 3, 4, 5, 10]")),
            id="[1, 2, 3, 4, 5].append(10): success case",
        ),
    ],
)
def test_parse_append_case(target_obj: ExprObj, attr_name: str, arg_objs: list[ExprObj, ...], expected):
    result = AttributeExpr.parse(target_obj, attr_name, arg_objs)

    assert result == expected
