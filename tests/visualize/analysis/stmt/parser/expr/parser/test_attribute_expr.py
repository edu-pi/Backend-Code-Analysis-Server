import pytest

from app.visualize.analysis.stmt.parser.expr.models.expr_obj import NameObj, ConstantObj, AttributeObj
from app.visualize.analysis.stmt.parser.expr.parser.attribute_expr import AttributeExpr


@pytest.mark.parametrize(
    "target, attr, args, expected",
    [
        pytest.param(
            NameObj(value="a", expressions=("a", "[1, 2, 3, 4, 5]")),
            "append",
            [ConstantObj(value=10, expressions=("10",))],
            AttributeObj(value="[1, 2, 3, 4, 5, 10]", expressions=("[1, 2, 3, 4, 5]", "[1, 2, 3, 4, 5, 10]")),
            id="a.append(10): success case",
        ),
        # Todo. 테스트 케이스 추가
    ],
)
def test_parse_append_case(target, attr, args, expected):
    result = AttributeExpr.parse(target, attr, args)

    assert result == expected
