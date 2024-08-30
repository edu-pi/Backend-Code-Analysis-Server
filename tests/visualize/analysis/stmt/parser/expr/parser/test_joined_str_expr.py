import pytest

from app.visualize.analysis.stmt.parser.expr.models.expr_obj import ExprObj, ConstantObj, FormattedValueObj
from app.visualize.analysis.stmt.parser.expr.parser.joined_str_expr import JoinedStrExpr


@pytest.mark.parametrize(
    "value_objs, expected",
    [
        pytest.param([], "", id="empty: success case"),
        pytest.param(
            [
                ConstantObj(value="i am ", expressions=("i am",)),
                FormattedValueObj(
                    value="song",
                    expressions=(
                        "{name}",
                        "song",
                    ),
                ),
            ],
            "i am song",
            id='f"i am {a}", success case',
        ),
        pytest.param(
            [
                FormattedValueObj(
                    value="30",
                    expressions=(
                        "{x}",
                        "30",
                    ),
                ),
                ConstantObj(value=" + ", expressions=(" + ",)),
                FormattedValueObj(
                    value="20",
                    expressions=(
                        "{y}",
                        "20",
                    ),
                ),
                ConstantObj(value=" = ", expressions=(" = ",)),
                FormattedValueObj(value="50", expressions=("{x + y}", "{30 + 20}", "50")),
            ],
            "30 + 20 = 50",
            id='f"{x} + {y} = {x + y}", success case',
        ),
    ],
)
def test_get_value(value_objs: list[ExprObj], expected):
    result = JoinedStrExpr._get_value(value_objs)

    assert result == expected


@pytest.mark.parametrize(
    "value_objs, value, expected",
    [
        pytest.param([], "", (), id="empty: success case"),
        pytest.param(
            [
                ConstantObj(value="i am ", expressions=("i am ",)),
                FormattedValueObj(
                    value="song",
                    expressions=(
                        "{name}",
                        "song",
                    ),
                ),
            ],
            "i am song",
            ("i am {name}", "i am song"),
            id='f"i am {a}", success case',
        ),
        pytest.param(
            [
                FormattedValueObj(
                    value="30",
                    expressions=(
                        "{x}",
                        "30",
                    ),
                ),
                ConstantObj(value=" + ", expressions=(" + ",)),
                FormattedValueObj(
                    value="20",
                    expressions=(
                        "{y}",
                        "20",
                    ),
                ),
                ConstantObj(value=" = ", expressions=(" = ",)),
                FormattedValueObj(value="50", expressions=("{x + y}", "{30 + 20}", "50")),
            ],
            "30 + 20 = 50",
            ("{x} + {y} = {x + y}", "30 + 20 = {30 + 20}", "30 + 20 = 50"),
            id='f"{x} + {y} = {x + y}", success case',
        ),
    ],
)
def test_concat_expressions(value_objs: list[ExprObj], value, expected):
    result = JoinedStrExpr._concat_expressions(value_objs, value)

    assert result == expected
