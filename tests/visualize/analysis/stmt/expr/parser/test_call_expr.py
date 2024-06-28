import pytest

from app.visualize.analysis.stmt.expr.model.expr_obj import ExprObj
from app.visualize.analysis.stmt.expr.model.range_expr_obj import RangeExpression, RangeExprObj
from app.visualize.analysis.stmt.expr.parser.call_expr import CallExpr


@pytest.mark.parametrize("func_name, args, keyword_arg_dict, expected", [])
def test_parse(func_name, args, keyword_arg_dict, expected):
    pass


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
    result = CallExpr._print_parse(args, keyword_arg_dict)

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
    result = CallExpr._apply_keywords(default_keyword, keyword_arg_dict)

    assert result == expected


@pytest.mark.parametrize(
    "expressions, expected_iter, expected_expressions",
    [
        (
                [
                    ExprObj(type="name", value=10, expressions=["a", "10"]),
                ],
                range(10),
                [
                    RangeExpression(start="0", end="a", step="1"),
                    RangeExpression(start="0", end="10", step="1")
                ]

        ),
        (
                [
                    ExprObj(type="name", value=3, expressions=["a", "3"]),
                    ExprObj(type="constant", value=10, expressions=["10"]),
                ],
                range(3, 10),
                [
                    RangeExpression(start="a", end="10", step="1"),
                    RangeExpression(start="3", end="10", step="1")
                ]

        ),
        (
                [
                    ExprObj(type="name", value=3, expressions=["a", "3"]),
                    ExprObj(type="constant", value=10, expressions=["10"]),
                    ExprObj(type="constant", value=2, expressions=["2"]),
                ],
                range(3, 10, 2),
                [
                    RangeExpression(start="a", end="10", step="2"),
                    RangeExpression(start="3", end="10", step="2")
                ]

        )
    ]
)
def test_range_parse(expressions, expected_iter, expected_expressions):
    result_iter, result_expressions = CallExpr._range_parse(expressions)

    assert result_iter == expected_iter
    assert result_expressions == expected_expressions


@pytest.mark.parametrize(
    "args, expected",
    [
        (["10"], RangeExpression(start="0", end="10", step="1")),
        (["a", "10"], RangeExpression(start="a", end="10", step="1")),
        (["a", "10", "2"], RangeExpression(start="a", end="10", step="2")),
        (["1", "10", "2"], RangeExpression(start="1", end="10", step="2")),
    ],
)
def test_create_range_dict(args, expected):
    result = CallExpr._create_range_expression(args)

    assert result == expected


@pytest.mark.parametrize(
    "arg_value_list, expected",
    [
        ([10], range(10)),
        ([3, 10], range(3, 10)),
        ([2, 10, 2], range(2, 10, 2)),
    ],
)
def test_create_range_iter(arg_value_list, expected):
    result = CallExpr._create_range_iter(arg_value_list)
    assert result == expected
