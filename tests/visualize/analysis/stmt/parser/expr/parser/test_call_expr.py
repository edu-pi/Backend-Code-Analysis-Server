import pytest

from app.visualize.analysis.stmt.parser.expr.models.expr_obj import AttributeObj, ExprObj


@pytest.mark.parametrize(
    "func_name, args, keyword_arg_dict, expected",
    [
        pytest.param(
            id="Built-in-function print: success case",
        ),
        pytest.param(
            id="Built-in-function range: success case",
        ),
        pytest.param(
            id="attribute-function append: success case",
        ),
    ],
)
def test_parse(func_name: str | AttributeObj, args: list[ExprObj], keyword_arg_dict: dict):
    pass


@pytest.mark.parametrize(
    "func_name, args, keyword_arg_dict, expected",
    [
        pytest.param(
            id="Built-in-function print: success case",
        ),
        pytest.param(
            id="Built-in-function range: success case",
        ),
    ],
)
def test_built_in_call_parse(func_name: str, args: list[ExprObj], keyword_arg_dict: dict):
    pass


@pytest.mark.parametrize(
    "attr_obj, args, keyword_arg_dict, expected",
    [
        pytest.param(
            id="attribute-function append: success case",
        ),
    ],
)
def test_attribute_call_parse(attr_obj: AttributeObj, args: list[ExprObj], keyword_arg_dict: dict):
    pass
