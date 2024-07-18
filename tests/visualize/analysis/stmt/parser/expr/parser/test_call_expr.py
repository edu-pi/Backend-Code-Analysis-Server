import pytest

from app.visualize.analysis.stmt.parser.expr.models.expr_obj import (
    AttributeObj,
    ExprObj,
    ConstantObj,
    PrintObj,
    RangeObj,
)
from app.visualize.analysis.stmt.parser.expr.models.range_expression import RangeExpression
from app.visualize.analysis.stmt.parser.expr.parser.built_in_func.print_expr import PrintExpr
from app.visualize.analysis.stmt.parser.expr.parser.built_in_func.range_expr import RangeExpr
from app.visualize.analysis.stmt.parser.expr.parser.call_expr import CallExpr


@pytest.mark.parametrize(
    "func_name, args, keyword_arg_dict, expected",
    [
        pytest.param(
            "print",
            [ConstantObj(value="Hello, World!", expressions=("Hello, World!",))],
            {},
            PrintObj(value="Hello, World!", expressions=("Hello, World!",)),
            id="Built-in-function print: success case",
        ),
        pytest.param(
            "range",
            [ConstantObj(value=5, expressions=("5",))],
            {},
            RangeObj(value=tuple(range(0, 5, 1)), expressions=(RangeExpression(start="0", end="5", step="1"),)),
            id="Built-in-function range: success case",
        ),
    ],
)
def test_built_in_parse(mocker, func_name: str | AttributeObj, args: list[ExprObj], keyword_arg_dict: dict, expected):
    mock_built_in_call_parse = mocker.patch.object(CallExpr, "_built_in_call_parse", return_value=expected)

    result = CallExpr.parse(func_name, args, keyword_arg_dict)

    assert result == expected
    mock_built_in_call_parse.assert_called_once_with(func_name, args, keyword_arg_dict)


@pytest.mark.parametrize(
    "func_name, args, keyword_arg_dict, expected",
    [
        pytest.param(
            "print",
            [ConstantObj(value="Hello, World!", expressions=("Hello, World!",))],
            {},
            PrintObj(value="Hello, World!", expressions=("Hello, World!",)),
            id="Built-in-function print: success case",
        ),
    ],
)
def test_built_in_print_call_parse(mocker, func_name: str, args: list[ExprObj], keyword_arg_dict: dict, expected):
    mock_print_expr_class = mocker.patch.object(PrintExpr, "parse", return_value=expected)

    result = CallExpr._built_in_call_parse(func_name, args, keyword_arg_dict)

    assert result == expected
    mock_print_expr_class.assert_called_once_with(args, keyword_arg_dict)


@pytest.mark.parametrize(
    "func_name, args, keyword_arg_dict, expected",
    [
        pytest.param(
            "range",
            [ConstantObj(value=5, expressions=("5",))],
            {},
            RangeObj(value=tuple(range(0, 5, 1)), expressions=(RangeExpression(start="0", end="5", step="1"),)),
            id="Built-in-function range: success case",
        ),
    ],
)
def test_built_in_range_call_parse(mocker, func_name: str, args: list[ExprObj], keyword_arg_dict: dict, expected):
    mock_range_expr_class = mocker.patch.object(RangeExpr, "parse", return_value=expected)

    result = CallExpr._built_in_call_parse(func_name, args, keyword_arg_dict)

    assert result == expected
    mock_range_expr_class.assert_called_once_with(args)


# @pytest.mark.parametrize(
#     "attr_obj, args, keyword_arg_dict, expected",
#     [
#         pytest.param(
#             id="attribute-function append: success case",
#         ),
#     ],
# )
# def test_attribute_call_parse(attr_obj: AttributeObj, args: list[ExprObj], keyword_arg_dict: dict, expected):
#     pass
