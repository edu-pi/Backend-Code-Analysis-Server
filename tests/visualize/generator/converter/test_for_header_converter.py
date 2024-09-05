import pytest

from app.visualize.analysis.stmt.parser.expr.models.expr_obj import ExprObj, ListObj
from app.visualize.analysis.stmt.parser.expr.models.expr_type import ExprType
from app.visualize.generator.converter.for_header_converter import ForHeaderConvertor
from app.visualize.generator.models.for_viz import ForConditionViz


@pytest.mark.parametrize(
    "iter_value, expected",
    [
        pytest.param([0, 1, 2, 3], ForConditionViz(target="mock", cur="0", start="0", end="3", step="1")),
        pytest.param(["A", "BB", "CCC"], ForConditionViz(target="mock", cur="A", start="A", end="CCC", step="1")),
    ],
)
def test__get_name_condition(iter_value, expected):
    mock_target_name = "mock"
    iter_obj = ExprObj(value=iter_value, expressions=(), type=ExprType.NAME)

    actual = ForHeaderConvertor._get_list_condition(mock_target_name, iter_obj)

    assert actual == expected


def test__get_condition(mocker):
    target = "i"
    iter_Obj = ListObj(value=[1, 2, 3, 4], expressions=("[1,2,3,4]",))
    mock_get_condition = mocker.patch.object(ForHeaderConvertor, "_get_list_condition")

    ForHeaderConvertor._get_condition(target, iter_Obj)

    mock_get_condition.assert_called_once_with(target, iter_Obj)


def test__get_list_condition():
    iter_Obj = ListObj(value=[0, 1, 2, 3, 4], expressions=("[0,1,2,3,4]",))

    actual = ForHeaderConvertor._get_list_condition("i", iter_Obj)

    assert isinstance(actual, ForConditionViz)
    assert actual.target == "i"
    assert actual.start == "0"
    assert actual.end == "4"
    assert actual.step == "1"
