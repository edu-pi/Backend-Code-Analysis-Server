from app.visualize.analysis.stmt_parser.expr_analysis.expr_models.expr_obj import ExprObj
from app.visualize.analysis.stmt_parser.expr_analysis.expr_parser.call_parser import CallParser, Range
import pytest


@pytest.mark.parametrize("arg, expect", [
    ([
         ExprObj(type="name", value=3, expressions=["a", "3"]),
         ExprObj(type="name", value=10, expressions=["10"]),
         ExprObj(type="name", value=2, expressions=["2"]), ],
     Range(value={'end': '10', 'start': '3', 'step': '2'},
           expressions=[{'end': '10', 'start': 'a', 'step': '2'},
                        {'end': '10', 'start': '3', 'step': '2'}])
    ),
    ([
         ExprObj(type="name", value=0, expressions=["0"]),
         ExprObj(type="name", value=10, expressions=["10"]),
         ExprObj(type="name", value=1, expressions=["1"]), ],
     Range(value={'end': '10', 'start': '0', 'step': '1'},
           expressions=[{'end': '10', 'start': '0', 'step': '1'}])
    )
])
def test__range_parse(arg, expect):
    """ ExprObj 리스트를 받아 Range 객체를 반환하는지 테스트"""
    actual = CallParser._range_parse(arg)
    assert actual == expect
