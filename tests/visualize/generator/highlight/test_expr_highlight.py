import pytest

from app.visualize.generator.highlight.expr_highlight import ExprHighlight


@pytest.mark.parametrize(
    "parsed_exprs, expected",
    [
        (["'*' * i+1", "'*' * 5", "*****"], [[0, 1, 2, 3, 4, 5, 6, 7, 8], [6], [0, 1, 2, 3, 4]]),
        (["1 + 2", "3"], [[0, 1, 2, 3, 4], [0]]),
        (["a + b + c", "10 + 20 + 30", "60"], [[0, 1, 2, 3, 4, 5, 6, 7, 8], [0, 1, 5, 6, 10, 11], [0, 1]]),
    ],
)
def test_get_highlight_attr(parsed_exprs, expected):
    result = ExprHighlight.get_highlight_attr(parsed_exprs)

    assert result == expected
