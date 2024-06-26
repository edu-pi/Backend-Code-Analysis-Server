import pytest

from app.visualize.analysis.stmt_parser.expr_analysis.expr_models.expr_obj import ExprObj
from app.visualize.analysis.stmt_parser.expr_analysis.expr_parser.call_parser import CallParser


@pytest.mark.parametrize("func_name, args, keyword_arg_dict, expected", [])
def test_parse(func_name, args, keyword_arg_dict, expected):
    assert True


@pytest.mark.parametrize(
    "args, keyword_arg_dict, expected",
    [
        ([ExprObj(type="constant", value="abc", expressions=["abc"])], {}, ["abc\n"]),
        (
            [
                ExprObj(type="constant", value="abc", expressions=["abc"]),
                ExprObj(type="constant", value=1, expressions=["1"]),
            ],
            {},
            ["abc 1\n"],
        ),
        (
            [
                ExprObj(type="constant", value="abc", expressions=["abc"]),
                ExprObj(type="name", value=3, expressions=["a", "3"]),
            ],
            {},
            ["abc a\n", "abc 3\n"],
        ),
        (
            [
                ExprObj(type="constant", value="abc", expressions=["abc"]),
                ExprObj(type="binop", value=3, expressions=["a + 1", "2 + 1", "3"]),
            ],
            {},
            ["abc a + 1\n", "abc 2 + 1\n", "abc 3\n"],
        ),
    ],
)
def test_print_parse(args, keyword_arg_dict, expected):
    result = CallParser._print_parse(args, keyword_arg_dict)

    assert result == expected


@pytest.mark.parametrize(
    "default_keyword, keyword_arg_dict, expected",
    [
        ({"sep": " ", "end": "\n"}, {}, {"sep": " ", "end": "\n"}),
        ({"sep": " ", "end": "\n"}, {"sep": "-"}, {"sep": "-", "end": "\n"}),
        ({"sep": " ", "end": "\n"}, {"end": " "}, {"sep": " ", "end": " "}),
        ({"sep": " ", "end": "\n"}, {"sep": "-", "end": " "}, {"sep": "-", "end": " "}),
    ],
)
def test_apply_keywords(default_keyword, keyword_arg_dict, expected):
    result = CallParser._apply_keywords(default_keyword, keyword_arg_dict)

    assert result == expected


@pytest.mark.parametrize(
    "expressions, expected",
    [
        (
            [
                ExprObj(type="name", value=3, expressions=["a", "3"]),
                ExprObj(type="constant", value=10, expressions=["10"]),
            ],
            [{"start": "a", "end": "10"}, {"start": "3", "end": "10"}],
        ),
        (
            [
                ExprObj(type="name", value=3, expressions=["a", "3"]),
                ExprObj(type="constant", value=10, expressions=["10"]),
                ExprObj(type="constant", value=2, expressions=["2"]),
            ],
            [{"start": "a", "end": "10", "step": "2"}, {"start": "3", "end": "10", "step": "2"}],
        ),
        (
            [
                ExprObj(type="name", value=0, expressions=["0"]),
                ExprObj(type="name", value=10, expressions=["10"]),
                ExprObj(type="name", value=1, expressions=["1"]),
            ],
            [{"start": "0", "end": "10", "step": "1"}],
        ),
    ],
)
def test_range_parse(expressions, expected):
    result = CallParser._range_parse(expressions)
    assert result == expected


@pytest.mark.parametrize(
    "args, expected",
    [
        (["10"], {"start": "0", "end": "10"}),
        (["a", "10"], {"start": "a", "end": "10"}),
        (["a", "10", "2"], {"start": "a", "end": "10", "step": "2"}),
        (["1", "10", "2"], {"start": "1", "end": "10", "step": "2"}),
    ],
)
def test_create_range_dict(args, expected):
    result = CallParser._create_range_dict(args)

    assert result == expected
