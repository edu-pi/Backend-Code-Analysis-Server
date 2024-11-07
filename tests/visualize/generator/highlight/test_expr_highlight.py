import pytest

from app.visualize.generator.highlight.expr_highlight import ExprHighlight


@pytest.mark.parametrize(
    "parsed_exprs, expected",
    [
        pytest.param(
            ["'*' * i+1", "'*' * 5", "*****"],
            [[0, 1, 2, 3, 4, 5, 6, 7, 8], [6], [0, 1, 2, 3, 4]],
            id="'*' * i+1: success case",
        ),
        pytest.param(["1 + 2", "3"], [[0, 1, 2, 3, 4], [0]], id="1 + 2: success case"),
        pytest.param(
            ["a + b + c", "10 + 20 + 30", "60"],
            [[0, 1, 2, 3, 4, 5, 6, 7, 8], [0, 1, 5, 6, 10, 11], [0, 1]],
            id="a + b + c: success case",
        ),
    ],
)
def test_get_highlight_attr(parsed_exprs, expected):
    result = ExprHighlight.get_highlight_indexes_exclusive_last(parsed_exprs)

    assert result == expected
