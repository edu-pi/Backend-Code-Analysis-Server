import pytest

from app.visualize.analysis.stmt.parser.expr.models.expr_obj import (
    ExprObj,
    ConstantObj,
    NameObj,
    BinopObj,
    PrintObj,
    RangeObj,
)
from app.visualize.analysis.stmt.parser.expr.models.range_expression import RangeExpression
from app.visualize.analysis.stmt.parser.expr.parser.call_expr import CallExpr


@pytest.mark.parametrize(
    "func_name, mock_value, mock_expressions",
    [
        pytest.param("print", "abc\n", ("abc",), id="print('abc'): success case"),
        pytest.param("print", "****\n", ("'*' * 4", "'****'"), id="print('*' * 4): success case"),
        pytest.param("print", "abc ", ("abc",), id="print('abc', end=' '): success case"),
        pytest.param("print", "abc def\n", ("abc def",), id="print('abc', 'def'): success case"),
        pytest.param("print", "abc-def\n", ("abc-def",), id="print('abc', 'def', sep='-'): success case"),
        pytest.param(
            "range",
            [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
            (RangeExpression(start="0", end="10", step="1")),
            id="range(10): success case",
        ),
        pytest.param(
            "range",
            [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
            (RangeExpression(start="0", end="a", step="1"), RangeExpression(start="0", end="10", step="1")),
            id="range(a): success case",
        ),
        pytest.param(
            "range",
            [2, 3, 4, 5, 6, 7, 8, 9],
            (RangeExpression(start="2", end="10", step="1")),
            id="range(2, 10): success case",
        ),
        pytest.param(
            "range",
            [2, 4, 6, 8],
            (RangeExpression(start="2", end="10", step="2")),
            id="range(2, 10, 2): success case",
        ),
    ],
)
def test_parse(mocker, func_name: str, mock_value, mock_expressions):
    mocker.patch(
        "app.visualize.analysis.stmt.parser.expr.parser.call_expr.CallExpr._print_parse",
        return_value=(mock_value, mock_expressions),
    )
    mocker.patch(
        "app.visualize.analysis.stmt.parser.expr.parser.call_expr.CallExpr._range_parse",
        return_value=(mock_value, mock_expressions),
    )
    result = CallExpr.parse(func_name, [mocker.MagicMock(spec=ExprObj)], {})

    assert isinstance(result, PrintObj) or isinstance(result, RangeObj)
    assert result.value == mock_value
    assert result.expressions == mock_expressions


@pytest.mark.parametrize(
    "args, keyword_arg_dict, expected",
    [
        pytest.param(
            [ConstantObj(value="abc", expressions=("abc",))], {}, ("abc\n", ("abc",)), id="print('abc'): success case"
        ),
        pytest.param(
            [
                ConstantObj(value="abc", expressions=("abc",)),
                ConstantObj(value=1, expressions=("1",)),
            ],
            {},
            ("abc 1\n", ("abc 1",)),
            id="print(abc, 1): success case",
        ),
        pytest.param(
            [
                ConstantObj(value="abc", expressions=("abc",)),
                NameObj(value=3, expressions=("a", "3")),
            ],
            {},
            (
                "abc 3\n",
                (
                    "abc a",
                    "abc 3",
                ),
            ),
            id="print(abc, a): success case",
        ),
        pytest.param(
            [
                ConstantObj(value="abc", expressions=("abc",)),
                BinopObj(value=3, expressions=("a + 1", "2 + 1", "3")),
            ],
            {},
            ("abc 3\n", ("abc a + 1", "abc 2 + 1", "abc 3")),
            id="print(abc,a + 1): success case",
        ),
        pytest.param(
            [
                ConstantObj(value="abc", expressions=("abc",)),
                NameObj(value=3, expressions=("a", "3")),
            ],
            {"sep": "-"},
            (
                "abc-3\n",
                (
                    "abc-a",
                    "abc-3",
                ),
            ),
            id="print(abc, a, sep='-'): success case",
        ),
    ],
)
def test_print_parse(args: list[ExprObj], keyword_arg_dict: dict, expected):
    result = CallExpr._print_parse(args, keyword_arg_dict)

    assert result == expected


@pytest.mark.parametrize(
    "default_keyword, keyword_arg_dict, expected",
    [
        pytest.param({"sep": " ", "end": "\n"}, {}, {"sep": " ", "end": "\n"}, id="default: success case"),
        pytest.param({"sep": " ", "end": "\n"}, {"sep": "-"}, {"sep": "-", "end": "\n"}, id="sep:'-': success case"),
        pytest.param({"sep": " ", "end": "\n"}, {"end": " "}, {"sep": " ", "end": " "}, id="end:' ': success case"),
        pytest.param(
            {"sep": " ", "end": "\n"},
            {"sep": "-", "end": " "},
            {"sep": "-", "end": " "},
            id="sep:'-', end:' ': success case",
        ),
    ],
)
def test_apply_keywords(default_keyword: dict, keyword_arg_dict: dict, expected):
    result = CallExpr._apply_keywords(default_keyword, keyword_arg_dict)

    assert result == expected


@pytest.mark.parametrize(
    "expressions, expected_iter, expected_expressions",
    [
        pytest.param(
            [
                NameObj(value=10, expressions=("a", "10")),
            ],
            tuple(range(10)),
            (RangeExpression(start="0", end="a", step="1"), RangeExpression(start="0", end="10", step="1")),
            id="range(a): success case",
        ),
        pytest.param(
            [
                NameObj(value=3, expressions=("a", "3")),
                ConstantObj(value=10, expressions=("10",)),
            ],
            tuple(range(3, 10)),
            (RangeExpression(start="a", end="10", step="1"), RangeExpression(start="3", end="10", step="1")),
            id="range(a, 10): success case",
        ),
        pytest.param(
            [
                NameObj(value=3, expressions=("a", "3")),
                ConstantObj(value=10, expressions=("10",)),
                ConstantObj(value=2, expressions=("2",)),
            ],
            tuple(range(3, 10, 2)),
            (RangeExpression(start="a", end="10", step="2"), RangeExpression(start="3", end="10", step="2")),
            id="range(a, 10, 2): success case",
        ),
    ],
)
def test_range_parse(expressions: list[ExprObj], expected_iter, expected_expressions):
    result_iter, result_expressions = CallExpr._range_parse(expressions)

    assert result_iter == expected_iter
    assert result_expressions == expected_expressions


@pytest.mark.parametrize(
    "args, expected",
    [
        pytest.param(["10"], RangeExpression(start="0", end="10", step="1"), id="range(10): success case"),
        pytest.param(["a", "10"], RangeExpression(start="a", end="10", step="1"), id="range(a, 10): success case"),
        pytest.param(
            ["a", "10", "2"], RangeExpression(start="a", end="10", step="2"), id="range(a, 10, 2): success case"
        ),
        pytest.param(
            ["1", "10", "2"], RangeExpression(start="1", end="10", step="2"), id="range(1, 10, 2): success case"
        ),
    ],
)
def test_create_range_dict(args: list, expected):
    result = CallExpr._create_range_expression(args)

    assert result == expected


@pytest.mark.parametrize(
    "arg_value_list, expected",
    [
        pytest.param([10], range(10), id="range(10): success case"),
        pytest.param([3, 10], range(3, 10), id="range(3, 10): success case"),
        pytest.param([2, 10, 2], range(2, 10, 2), id="range(2, 10, 2): success case"),
    ],
)
def test_create_range_iter(arg_value_list: list, expected):
    result = CallExpr._create_range_iter(arg_value_list)
    assert result == expected
