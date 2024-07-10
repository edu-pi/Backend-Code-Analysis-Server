import pytest

from app.visualize.utils import utils


@pytest.mark.parametrize(
    "expressions, expected",
    [
        pytest.param(
            [("10",), ("a + 13", "5 + 13", "28"), ("b", "4")],
            [("10", "a + 13", "b"), ("10", "5 + 13", "4"), ("10", "28", "4")],
            id="[['10'], ['a + 13', '5 + 13', '28'], ['b', '4']] success case",
        ),
        pytest.param(
            [("a", "10"), ("b", "20"), ("30",)],
            [("a", "b", "30"), ("10", "20", "30")],
            id="[['a', '10'], ['b', '20'], ['30']] success case",
        ),
        pytest.param(
            [("10",), ("20",)],
            [("10", "20")],
            id="[('10',), ('20',)] success case",
        ),
    ],
)
def test_transpose_with_last_fill(expressions, expected):
    result = utils.transpose_with_last_fill(expressions)

    assert result == expected
