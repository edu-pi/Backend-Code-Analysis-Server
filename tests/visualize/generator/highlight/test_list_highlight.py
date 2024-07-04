import pytest

from app.visualize.generator.highlight.list_highlight import ListHighlight


class TestListHighlight:

    @staticmethod
    @pytest.mark.parametrize(
        "parsed_exprs, expected",
        [
            (["['Hello','World']"], [[0, 1], [0, 1]]),
            (["[1,2,3]"], [[0, 1, 2], [0, 1, 2]]),
            (["[a + 1,b]", "[3 + 1,4]", "[4,4]"], [[0, 1], [0, 1], [0], [0, 1]]),
        ],
    )
    def test_get_highlight_attr(parsed_exprs, expected):
        result = ListHighlight.get_highlight_indexes(parsed_exprs)

        assert result == expected
